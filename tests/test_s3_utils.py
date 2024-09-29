import pytest
from unittest.mock import patch, MagicMock
from src.s3_utils import stream_s3_file

@patch('src.s3_utils.s3_client')
def test_stream_s3_file(mock_s3_client):
    mock_body = MagicMock()
    mock_body.iter_lines.return_value = [b'{"event": "data"}']
    mock_s3_client.get_object.return_value = {'Body': mock_body}
    lines = list(stream_s3_file('bucket', 'key'))
    assert len(lines) == 1
    assert lines[0] == '{"event": "data"}'
    mock_s3_client.get_object.assert_called_once_with(Bucket='bucket', Key='key')
