import pytest
from unittest.mock import patch
from src.event_processor import process_event, process_event_batch
import json

def test_process_event_valid():
    valid_event = json.dumps({
        "user_id": "123e4567-e89b-12d3-a456-426614174000",
        "event_type": "purchase",
        "event_time": "2023-10-01T12:34:56Z",
        "event_properties": {"item": "book"},
        "user_properties": {"name": "John Doe"}
    })
    result, event_data = process_event(valid_event)
    assert result == "valid"
    assert event_data['user_id'] == "123e4567-e89b-12d3-a456-426614174000"

def test_process_event_invalid_json():
    invalid_event = '{"user_id": "123", "event_type": "purchase"'
    result, event_data = process_event(invalid_event)
    assert result == "invalid"
    assert event_data is None

def test_process_event_invalid_schema():
    invalid_event = json.dumps({
        "user_id": "123",
        "event_type": "purchase",
        "event_time": "invalid-time",
        "event_properties": {},
        "user_properties": {}
    })
    result, event_data = process_event(invalid_event)
    assert result == "invalid"
    assert event_data is None

@patch('src.event_processor.save_events_batch_to_db')
@patch('src.event_processor.save_user_profiles_batch_to_db')
def test_process_event_batch(mock_save_user_profiles, mock_save_events_batch):
    event_batch = [
        json.dumps({
            "user_id": "123e4567-e89b-12d3-a456-426614174000",
            "event_type": "login",
            "event_time": "2023-10-01T12:34:56Z",
            "event_properties": {},
            "user_properties": {}
        }),
        json.dumps({
            "user_id": "invalid-uuid",
            "event_type": "logout",
            "event_time": "2023-10-01T12:34:56Z",
            "event_properties": {},
            "user_properties": {}
        })
    ]
    event_type_count = {}
    valid_events, invalid_events, error_count = process_event_batch(event_batch, event_type_count)
    assert valid_events == 1
    assert invalid_events == 1
    assert error_count == 0
    mock_save_user_profiles.assert_called_once()
    mock_save_events_batch.assert_called_once()
