import json
import time
from jsonschema import validate, ValidationError
import dateutil.parser
from uuid import UUID
from concurrent.futures import ThreadPoolExecutor
from .db_utils import save_events_batch_to_db, save_user_profiles_batch_to_db
from .aws_utils import publish_cloudwatch_metric
from .s3_utils import stream_s3_file
from .logger import logger

# Schema for event validation
event_schema = {
    "type": "object",
    "properties": {
        "user_id": {"type": "string", "format": "uuid"},
        "event_type": {"type": "string"},
        "event_time": {"type": "string", "format": "date-time"},
        "event_properties": {"type": "object"},
        "user_properties": {"type": "object"}
    },
    "required": ["user_id", "event_type", "event_time", "event_properties", "user_properties"]
}

def validate_uuid(uuid_string):
    try:
        UUID(uuid_string)
        return True
    except ValueError:
        return False

def process_event(event):
    """Process individual event in a separate process."""
    try:
        event_data = json.loads(event)
        
        # Validate schema (including UUID and ISO 8601 format checks)
        validate(instance=event_data, schema=event_schema)

        # UUID Validation
        if not validate_uuid(event_data['user_id']):
            logger.error(f"Invalid UUID for event: {event_data['user_id']}")
            return "invalid", None

        # Validate event_time format using dateutil.parser
        try:
            event_data['event_time'] = dateutil.parser.isoparse(event_data['event_time']).isoformat()
        except ValueError:
            logger.error(f"Invalid event_time for event: {event_data}.")
            return "invalid", None

        return "valid", event_data
    
    except (json.JSONDecodeError, ValidationError) as e:
        logger.error(f"Invalid event: {event}, error: {str(e)}")
        return "invalid", None
    except Exception as e:
        logger.error(f"Unexpected error while processing event: {event}, error: {str(e)}")
        return "error", None

def process_event_batch(event_batch, event_type_count):
    """Process a batch of events together."""
    logger.info(f"Processing batch of {len(event_batch)} events")

    valid_events = 0
    invalid_events = 0
    error_count = 0

    processed_events = []

    # Process the entire batch in parallel
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_event, event) for event in event_batch]
        for future in futures:
            result, event_data = future.result()

            if result == "valid":
                valid_events += 1
                event_type_count[event_data['event_type']] = event_type_count.get(event_data['event_type'], 0) + 1
                processed_events.append(event_data)
            elif result == "invalid":
                invalid_events += 1
            else:
                error_count += 1

    # Save the valid events and user profiles in batch
    if processed_events:
        save_user_profiles_batch_to_db(processed_events)
        save_events_batch_to_db(processed_events)

    # Return updated counts
    return valid_events, invalid_events, error_count

def process_s3_file(bucket, key, batch_size):
    """Download and process the JSONL file from S3 using stream and true batch inserts."""
    logger.info(f"Downloading and processing file {key} from bucket {bucket}")

    # Start processing timer
    start_time = time.time()

    # Initialize metrics
    total_valid_events = 0
    total_invalid_events = 0
    total_error_count = 0
    event_type_count = {}

    event_batch = []

    try:
        # Stream lines from S3
        for event in stream_s3_file(bucket, key):
            event_batch.append(event)

            # Once batch is full, process the entire batch
            if len(event_batch) >= batch_size:
                valid_events, invalid_events, error_count = process_event_batch(event_batch, event_type_count)
                total_valid_events += valid_events
                total_invalid_events += invalid_events
                total_error_count += error_count
                event_batch.clear()

        # Process any remaining events in the batch
        if event_batch:
            valid_events, invalid_events, error_count = process_event_batch(event_batch, event_type_count)
            total_valid_events += valid_events
            total_invalid_events += invalid_events
            total_error_count += error_count

    except Exception as e:
        logger.error(f"Error processing file from S3: {str(e)}")
        return

    # Log aggregated results
    logger.info(f"Processed {total_valid_events} valid events, {total_invalid_events} invalid events, {total_error_count} errors.")

    # Log the total processing time
    end_time = time.time()
    processing_time = end_time - start_time
    logger.info(f"Total processing time for file {key}: {processing_time:.2f} seconds")

    # Publish aggregated CloudWatch metrics once
    publish_cloudwatch_metric("ValidEvents", total_valid_events)
    publish_cloudwatch_metric("InvalidEvents", total_invalid_events)
    publish_cloudwatch_metric("ErrorEvents", total_error_count)

    for event_type, count in event_type_count.items():
        publish_cloudwatch_metric(f"EventType-{event_type}", count)