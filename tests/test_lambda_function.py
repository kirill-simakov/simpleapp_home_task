import pytest
from unittest.mock import patch
from src.lambda_function import lambda_handler

@patch('src.lambda_function.process_sqs_message')
def test_lambda_handler(mock_process_sqs_message):
    event = {'Records': []}  # Sample event
    context = None
    response = lambda_handler(event, context)
    mock_process_sqs_message.assert_called_once_with(event)
    assert response['statusCode'] == 200
