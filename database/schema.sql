-- Market prices cache
CREATE TABLE IF NOT EXISTS market_prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    state TEXT NOT NULL,
    district TEXT NOT NULL,
    commodity TEXT NOT NULL,
    modal_price REAL,
    min_price REAL,
    max_price REAL,
    variety TEXT,
    grade TEXT,
    market_date DATE,
    cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Location validation cache
CREATE TABLE IF NOT EXISTS districts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    state TEXT NOT NULL,
    district TEXT NOT NULL,
    normalized_name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Chat sessions
CREATE TABLE IF NOT EXISTS chat_sessions (
    session_id TEXT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    first_message TEXT,
    message_count INTEGER DEFAULT 0
);

-- Chat messages
CREATE TABLE IF NOT EXISTS chat_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    user_message TEXT NOT NULL,
    assistant_response TEXT NOT NULL,
    chat_data JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES chat_sessions(session_id)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_market_prices_lookup ON market_prices(state, district, commodity, market_date);
CREATE INDEX IF NOT EXISTS idx_districts_lookup ON districts(state, district);
CREATE INDEX IF NOT EXISTS idx_chat_messages_session ON chat_messages(session_id);
