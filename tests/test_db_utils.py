import pytest
from unittest.mock import patch, MagicMock
from src.db_utils import save_events_batch_to_db, save_user_profiles_batch_to_db

@pytest.fixture
def mock_db_conn():
    with patch('src.db_utils.get_db_connection') as mock_get_conn, \
         patch('src.db_utils.release_db_connection') as mock_release_conn:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn
        yield mock_cursor
        mock_cursor.close.assert_called_once()
        mock_conn.commit.assert_called_once()
        mock_release_conn.assert_called_once_with(mock_conn)

def test_save_events_batch_to_db(mock_db_conn):
    events_batch = [{
        'user_id': '123e4567-e89b-12d3-a456-426614174000',
        'event_type': 'purchase',
        'event_time': '2023-10-01T12:34:56Z',
        'event_properties': {"item": "book"}
    }]
    save_events_batch_to_db(events_batch)
    mock_db_conn.executemany.assert_called_once()

def test_save_user_profiles_batch_to_db(mock_db_conn):
    user_profiles_batch = [{
        'user_id': '123e4567-e89b-12d3-a456-426614174000',
        'user_properties': {"name": "Jane"},
        'event_time': '2023-10-01T12:34:56Z'
    }]
    save_user_profiles_batch_to_db(user_profiles_batch)
    mock_db_conn.executemany.assert_called_once()
