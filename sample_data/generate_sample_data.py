import json
import uuid
from datetime import datetime, timedelta
import random

# Generate random user profiles and events, with an option to generate invalid events
def generate_random_event(user_id, valid=True):
    event_types = ["purchase", "login", "logout", "signup"]
    event_type = random.choice(event_types)
    
    # Generate random event properties and user properties
    event_properties = {
        "amount": round(random.uniform(10, 500), 2),
        "currency": random.choice(["USD", "EUR", "GBP"]),
        "item": random.choice(["book", "laptop", "shoes", "phone", "headphones"]),
    } if event_type == "purchase" else {}
    
    user_properties = {
        "name": random.choice(["Alice", "Bob", "Charlie", "David"]),
        "language": random.choice(["EN", "DE", "FR"]),
        "location": random.choice(["Berlin", "Paris", "London", "Madrid"]),
    }

    event_time = datetime.now() - timedelta(days=random.randint(0, 365))
    
    # Generate invalid events with missing or incorrect data
    if not valid:
        error_type = random.choice(["missing_field", "incorrect_type"])
        
        if error_type == "missing_field":
            # Randomly remove a required field (user_id, event_type, event_time, etc.)
            fields = ["user_id", "event_type", "event_time", "event_properties", "user_properties"]
            field_to_remove = random.choice(fields)
            event = {
                "user_id": str(user_id),  # Convert UUID to string
                "event_type": event_type,
                "event_time": event_time.isoformat(),
                "event_properties": event_properties,
                "user_properties": user_properties
            }
            del event[field_to_remove]  # Remove a required field
            return event
        
        elif error_type == "incorrect_type":
            # Introduce a wrong data type for a key
            event = {
                "user_id": str(user_id) if random.random() > 0.5 else 12345,  # Incorrect type: int instead of UUID string
                "event_type": event_type,
                "event_time": "InvalidDate" if random.random() > 0.5 else event_time.isoformat(),  # Invalid datetime format
                "event_properties": event_properties,
                "user_properties": user_properties
            }
            return event

    # Return a valid event if no errors are introduced
    return {
        "user_id": str(user_id),  # Convert UUID to string
        "event_type": event_type,
        "event_time": event_time.isoformat(),
        "event_properties": event_properties,
        "user_properties": user_properties
    }

# Create sample data with both valid and invalid events
def generate_test_jsonl_data(num_rows, invalid_event_percentage, unique_users, file_name):
    user_ids = [uuid.uuid4() for _ in range(unique_users)]
    jsonl_data = []
    
    for _ in range(num_rows):
        user_id = random.choice(user_ids)
        # Generate invalid events based on the specified percentage
        valid = random.random() > invalid_event_percentage
        event = generate_random_event(user_id, valid)
        jsonl_data.append(json.dumps(event))
    
    with open(file_name, "w") as file:
        file.write("\n".join(jsonl_data))

    print(f"Sample JSONL data with invalid events saved to {file_name}")

# Generate and save sample data locally
generate_test_jsonl_data(num_rows=10000, invalid_event_percentage=0.3, unique_users=700, file_name="sample_data/sample_events.jsonl")
