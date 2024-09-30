# Event Processing Service

This project is an AWS Lambda Python service for processing and aggregating events from S3. It validates events, saves user profiles and valid events to a PostgreSQL database, and records metrics and logs.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup Guide](#setup-guide)
- [Running the Service](#running-the-service)
- [Testing](#testing)

## Prerequisites

Before you begin, ensure you have the following installed on your local machine:

- **Docker and Docker Compose**: To run services in containers.
- **Python 3.7+**: For running scripts and tests.
- **Pipenv**: For managing Python virtual environments and dependencies.

### Install Pipenv

If you don't have Pipenv installed, you can install it using pip:

```bash
pip install pipenv
```

## Setup Guide

### 1. Clone the Repository

Clone the project repository to your local machine.

### 2. Install Python Dependencies

Use Pipenv to create a virtual environment and install dependencies:

```bash
pipenv install
```

This will create a Pipenv virtual environment and install all required packages specified in the Pipfile.

### 3. Activate the Virtual Environment

Activate the Pipenv shell:

```bash
pipenv shell
```

## Running the Service

### 1. Build and Start Docker Containers

Use Docker Compose to build and run the necessary services:

```bash
docker compose up -d
```

This command will:

- Build the Docker images specified in `docker-compose.yml`.
- Start the containers in detached mode (`-d`).

### 2. Verify Services are Running

Check that the Docker containers are running:

```bash
docker ps
```

You should see containers for:

- **PostgreSQL**: The database service.
- **LocalStack**: A local AWS cloud stack emulator.
- **Lambda Function**: The AWS Lambda function container.

## Testing

### 1. Generate Sample Data

Generate sample event data for testing:

```bash
python sample_data/generate_sample_data.py
```

This script generates sample events and saves them to `sample_data/sample_events.jsonl`.

### 2. Run Unit Tests

Execute the test suite using pytest:

```bash
pytest
```

This will run all tests located in the `tests/` directory.

### 3. Run Integration Test

Execute the integration test script:

```bash
python test_lambda_integration.py
```

This script performs the following steps:

- Uploads sample event data to the local S3 bucket.
- Sends a message to the local SQS queue to trigger the Lambda function.
- Invokes the Lambda handler directly to process the events.

### 4. Check Test Results

- **Logs**: You can view the Lambda function logs in the console.

- **Database**: Connect to the PostgreSQL database to verify that events and user profiles have been saved correctly.

```bash
docker exec -it <postgres_container_id> psql -U postgres -d events_db
```

Replace `<postgres_container_id>` with the actual container ID or name.
