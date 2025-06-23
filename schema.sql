CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    title TEXT,
    content TEXT,
    start_time TEXT,
    username TEXT
);

CREATE TABLE event_styles (
    id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES events(id) ON DELETE CASCADE,
    style TEXT
);

CREATE TABLE styles (
    id INTEGER PRIMARY KEY,
    style TEXT
);

CREATE TABLE event_participants (
    id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES events(id),
    username TEXT
);

CREATE INDEX idx_event_participants ON event_participants (event_id);
CREATE INDEX idx_username ON events (username);
CREATE INDEX idx_username_part ON event_participants (username);