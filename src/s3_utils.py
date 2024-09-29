from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
import boto3
from .config import CHUNK_SIZE
from .aws_utils import s3_client
from .logger import logger

@retry(
    stop=stop_after_attempt(5),
    wait=wait_fixed(2),
    retry=retry_if_exception_type((boto3.exceptions.Boto3Error, Exception))
)
def stream_s3_file(bucket, key, chunk_size=CHUNK_SIZE):
    """Stream lines from S3 file in a memory-efficient way using yield with retry."""
    try:
        response = s3_client.get_object(Bucket=bucket, Key=key)
        for line in response['Body'].iter_lines(chunk_size=chunk_size):
            if line:
                yield line.decode('utf-8')
    except Exception as e:
        logger.error(f"Error streaming file from S3: {str(e)}")
        raise