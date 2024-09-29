import subprocess
from src.lambda_function import lambda_handler

# 1. Upload file to S3 using awslocal
def upload_file_to_s3():
    print("Uploading file to S3 bucket...")
    s3_command = "awslocal s3 cp sample_data/sample_events.jsonl s3://event-bucket/sample_events.jsonl"
    result = subprocess.run(s3_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        print("File uploaded successfully.")
    else:
        print(f"Error uploading file to S3: {result.stderr.decode('utf-8')}")

# 2. Send an SQS message using awslocal
def send_sqs_message():
    print("Sending SQS message...")
    sqs_command = """
    awslocal sqs send-message \
    --queue-url http://localhost:4566/000000000000/event-notification-queue \
    --message-body '{"Records": [{"s3": {"bucket": {"name": "event-bucket"}, "object": {"key": "sample_events.jsonl"}}}]}'
    """
    result = subprocess.run(sqs_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        print("SQS message sent successfully.")
    else:
        print(f"Error sending SQS message: {result.stderr.decode('utf-8')}")

# 3. Invoke Lambda function directly in Python
def invoke_lambda_directly():
    print("Invoking Lambda handler directly...")

    # Simulated SQS event payload
    event_payload = {
        "Records": [
            {
                "s3": {
                    "bucket": {
                        "name": "event-bucket"
                    },
                    "object": {
                        "key": "sample_events.jsonl"
                    }
                }
            }
        ]
    }

    # Call the lambda handler directly
    response = lambda_handler(event_payload, None)
    print(f"Lambda Response: {response}")

# Main function to run all steps
if __name__ == "__main__":
    upload_file_to_s3()          # Step 1: Upload file to S3
    send_sqs_message()           # Step 2: Send SQS message
    invoke_lambda_directly()     # Step 3: Invoke Lambda directly
