import boto3
from botocore.config import Config
from botocore.exceptions import NoCredentialsError
from .config import AWS_REGION, S3_ENDPOINT_URL, SQS_ENDPOINT_URL
from .logger import logger

# Adding retry configuration for S3 client
config = Config(
    retries={'max_attempts': 10, 'mode': 'standard'},
    connect_timeout=300,
    read_timeout=300
)

# Initialize AWS clients
s3_client = boto3.client('s3', region_name=AWS_REGION, endpoint_url=S3_ENDPOINT_URL,
                         aws_access_key_id='fake_access_key',
                         aws_secret_access_key='fake_secret_key',
                         config=config)

sqs_client = boto3.client('sqs', region_name=AWS_REGION, endpoint_url=SQS_ENDPOINT_URL,
                          aws_access_key_id='fake_access_key',
                          aws_secret_access_key='fake_secret_key')

cloudwatch = boto3.client('cloudwatch', region_name=AWS_REGION, endpoint_url=S3_ENDPOINT_URL,
                          aws_access_key_id='fake_access_key',
                          aws_secret_access_key='fake_secret_key')

def publish_cloudwatch_metric(metric_name, value, unit="Count"):
    """Send custom metric data to CloudWatch."""
    try:
        cloudwatch.put_metric_data(
            Namespace='EventProcessing',
            MetricData=[
                {
                    'MetricName': metric_name,
                    'Value': value,
                    'Unit': unit
                }
            ]
        )
        logger.info(f"Published metric: {metric_name} with value: {value}")
    except NoCredentialsError:
        logger.error("No AWS credentials available for CloudWatch.")
