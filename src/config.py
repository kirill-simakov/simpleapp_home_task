import os
from .logger import logger

AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
LOCALSTACK_HOSTNAME = os.getenv("LOCALSTACK_HOSTNAME", "localhost")

SQS_ENDPOINT_URL = f"http://{LOCALSTACK_HOSTNAME}:4566"
S3_ENDPOINT_URL = f"http://{LOCALSTACK_HOSTNAME}:4566"

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "events_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")

# Constants for processing events
CHUNK_SIZE = 1024
BATCH_SIZE = 1000

logger.info("Configuration loaded")