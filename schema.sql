DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT,
    image BLOB
);

DROP TABLE IF EXISTS events;
CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    title TEXT,
    content TEXT,
    start_time TEXT,
    username TEXT REFERENCES users(username) ON DELETE CASCADE
);

DROP TABLE IF EXISTS event_styles;
CREATE TABLE event_styles (
    id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES events(id) ON DELETE CASCADE,
    style TEXT
);

DROP TABLE IF EXISTS styles;
CREATE TABLE styles (
    id INTEGER PRIMARY KEY,
    style TEXT
);

DROP TABLE IF EXISTS event_participants;
CREATE TABLE event_participants (
    id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES events(id) ON DELETE CASCADE,
    username TEXT
);

DROP INDEX IF EXISTS idx_event_participants;
DROP INDEX IF EXISTS idx_username;
DROP INDEX IF EXISTS idx_username_part;
CREATE INDEX idx_event_participants ON event_participants (event_id);
CREATE INDEX idx_username ON events (username);
CREATE INDEX idx_username_part ON event_participants (username);