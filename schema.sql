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
    event_id INTEGER REFERENCES events(id),
    style TEXT
);

CREATE TABLE event_participants (
    id INTEGER PRIMARY KEY,
    event_id INTEGER REFERENCES events(id),
    username TEXT
);