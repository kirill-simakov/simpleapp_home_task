FROM public.ecr.aws/lambda/python:3.11

# Set the working directory
WORKDIR /var/task

# Copy the src folder to the Lambda task root
COPY src/ ${LAMBDA_TASK_ROOT}

# Copy requirements.txt to the root directory
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the Lambda function handler as the entry point for AWS Lambda
CMD ["lambda_function.lambda_handler"]