import json
from .event_processor import process_s3_file
from .config import BATCH_SIZE
from .logger import logger

def process_sqs_message(event):
    """Process SQS message, download the S3 file, validate and save events."""
    for record in event['Records']:
        s3_bucket = record['s3']['bucket']['name']
        s3_key = record['s3']['object']['key']
        
        logger.info(f"Processing file from S3: {s3_key} in bucket {s3_bucket}")
        process_s3_file(s3_bucket, s3_key, BATCH_SIZE)

def lambda_handler(event, context):
    """Lambda handler function to process SQS messages."""
    logger.info(f"Received event: {json.dumps(event)}")
    process_sqs_message(event)

    return {
        'statusCode': 200,
        'body': json.dumps('Events processed successfully.')
    }