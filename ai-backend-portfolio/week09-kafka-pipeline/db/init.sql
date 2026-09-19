CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    event_id VARCHAR(50) UNIQUE NOT NULL,
    event_type VARCHAR(50),
    raw_payload JSONB,
    classified_type VARCHAR(50),
    entities JSONB,
    anomaly_score DECIMAL(3,2),
    processed_at TIMESTAMP DEFAULT NOW()
);
