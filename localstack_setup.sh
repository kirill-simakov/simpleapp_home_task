#!/bin/bash

# Create S3 bucket
awslocal s3 mb s3://event-bucket

# Create SQS queue
awslocal sqs create-queue --queue-name event-notification-queue

echo "LocalStack S3 and SQS resources initialized."
