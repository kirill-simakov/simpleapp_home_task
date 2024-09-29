CREATE TABLE IF NOT EXISTS user_profile (
    user_id UUID PRIMARY KEY,
    user_properties JSONB,
    last_updated_time TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS events (
    event_id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    event_time TIMESTAMP NOT NULL,
    event_properties JSONB,
    CONSTRAINT fk_user
        FOREIGN KEY(user_id) 
        REFERENCES user_profile(user_id)
);

CREATE INDEX IF NOT EXISTS idx_event_time ON events(event_time);
