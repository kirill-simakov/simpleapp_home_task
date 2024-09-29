import pytest
from unittest.mock import patch, MagicMock
from src.aws_utils import publish_cloudwatch_metric

@patch('src.aws_utils.cloudwatch')
def test_publish_cloudwatch_metric(mock_cloudwatch_client):
    mock_cloudwatch_client.put_metric_data.return_value = {}
    
    # Invoke the function
    publish_cloudwatch_metric("TestMetric", 1)
    
    # Assert that put_metric_data was called with correct parameters
    mock_cloudwatch_client.put_metric_data.assert_called_once()
    args, kwargs = mock_cloudwatch_client.put_metric_data.call_args
    assert kwargs['Namespace'] == 'EventProcessing'
    metric_data = kwargs['MetricData'][0]
    assert metric_data['MetricName'] == 'TestMetric'
    assert metric_data['Value'] == 1
