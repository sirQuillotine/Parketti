import db

def add_event(title, content, start_time, username, styles):
    sql = "INSERT INTO events (title, content, start_time, username) VALUES (?, ?, ?, ?)"
    db.execute(sql, [title, content, start_time, username])
    event_id = db.last_insert_id()

    sql = "INSERT INTO event_styles (event_id, style) VALUES (?, ?)"
    for style in styles:
        db.execute(sql, [event_id, style])
    return event_id

def get_event_styles(event_id):
    sql = """SELECT s.id, s.style FROM event_styles s where s.event_id = ?"""
    return db.query(sql, [event_id])

def get_event_participants(event_id):
    sql = """SELECT s.id, s.username FROM event_participants s where s.event_id = ?"""
    result = db.query(sql, [event_id])
    return [row[1] for row in result] if result else []

def get_events(page, page_size):
    sql = """SELECT e.id, e.title, e.content, e.start_time, e.username
             FROM events e LIMIT ? OFFSET ?
             """
    return db.query(sql, [page_size, (page - 1) * page_size])

def get_user_events(username, page, page_size):
    sql = """SELECT e.id, e.title, e.content, e.start_time, e.username
             FROM events e WHERE e.username = ? LIMIT ? OFFSET ?"""
    return db.query(sql, [username, page_size, (page - 1) * page_size])

def get_user_participations(username, page, page_size):
    sql = """SELECT e.id, e.title, e.content, e.start_time, e.username
             FROM events e
             JOIN event_participants ep ON e.id = ep.event_id
             WHERE ep.username = ? LIMIT ? OFFSET ?"""
    return db.query(sql, [username,  page_size, (page - 1) * page_size])

def search_events(search, page, page_size):
    sql = """SELECT e.id, e.title, e.content, e.start_time, e.username
             FROM events e WHERE e.title LIKE ? OR e.content LIKE ? LIMIT ? OFFSET ?"""
    return db.query(sql, ["%" + search + "%", "%" + search + "%", page_size, (page - 1) * page_size])

def get_event(event_id):
    sql = """SELECT e.id, e.title, e.content, e.start_time, e.username
             FROM events e WHERE e.id = ?"""
    return db.query(sql, [event_id])[0]

def get_event_count():
    sql = """SELECT COUNT(*) FROM events"""
    return db.query(sql)[0][0]

def get_user_event_count(username):
    sql = """SELECT COUNT(*) FROM events WHERE username = ?"""
    return db.query(sql, [username])[0][0]

def get_user_participation_count(username):
    sql = """SELECT COUNT(*) FROM event_participants ep
             JOIN events e ON ep.event_id = e.id
             WHERE ep.username = ?"""
    return db.query(sql, [username])[0][0]

def update_event(event_id, title, content, start_time, styles):
    sql = """UPDATE events SET title = ?, content = ?, start_time = ? WHERE id = ?"""
    db.execute(sql, [title, content, start_time, event_id])

    sql = """DELETE FROM event_styles WHERE event_id = ?"""
    db.execute(sql, [event_id])

    sql = """INSERT INTO event_styles (event_id, style) VALUES (?, ?)"""
    for style in styles:
        db.execute(sql, [event_id, style])

def delete_event(event_id):
    sql = """DELETE FROM events WHERE id = ?"""
    db.execute(sql, [event_id])

def add_style(event_id, style):
    sql = """INSERT INTO event_styles (event_id, style) VALUES (?, ?)"""
    db.execute(sql, [event_id, style])

def add_participants(event_id, username):
    sql = """INSERT INTO event_participants (event_id, username) VALUES (?, ?)"""
    db.execute(sql, [event_id, username])

def delete_participant(event_id, username):
    sql = """DELETE FROM event_participants WHERE event_id = ? AND username = ?"""
    db.execute(sql, [event_id, username])
