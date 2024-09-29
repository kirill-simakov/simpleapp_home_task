import psycopg2
from psycopg2 import pool
import json
from .config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD
from .logger import logger

# Initialize PostgreSQL connection pool
db_pool = psycopg2.pool.SimpleConnectionPool(1, 50, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, database=DB_NAME)

def get_db_connection():
    """Get a connection from the pool."""
    return db_pool.getconn()

def release_db_connection(conn):
    """Release the connection back to the pool."""
    db_pool.putconn(conn)

def save_events_batch_to_db(events_batch):
    """Insert a batch of valid events into the events table."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        insert_event_query = """
        INSERT INTO events (user_id, event_type, event_time, event_properties)
        VALUES (%s, %s, %s, %s)
        """
        cursor.executemany(insert_event_query, [
            (event['user_id'], event['event_type'], event['event_time'], json.dumps(event['event_properties']))
            for event in events_batch
        ])
        conn.commit()
    except Exception as e:
        logger.error(f"Error inserting batch of events: {str(e)}")
        conn.rollback()
    finally:
        cursor.close()
        release_db_connection(conn)

def save_user_profiles_batch_to_db(user_profiles_batch):
    """Insert or update a batch of user profiles in the user_profile table."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        insert_user_query = """
        INSERT INTO user_profile (user_id, user_properties, last_updated_time)
        VALUES (%s, %s, %s)
        ON CONFLICT (user_id)
        DO UPDATE SET
            user_properties = EXCLUDED.user_properties,
            last_updated_time = EXCLUDED.last_updated_time
        WHERE user_profile.last_updated_time IS NULL
            OR EXCLUDED.last_updated_time > user_profile.last_updated_time;
        """
        cursor.executemany(insert_user_query, [
            (profile['user_id'], json.dumps(profile['user_properties']), profile['event_time'])
            for profile in user_profiles_batch
        ])
        conn.commit()
    except Exception as e:
        logger.error(f"Error inserting batch of user profiles: {str(e)}")
        conn.rollback()
    finally:
        cursor.close()
        release_db_connection(conn)
