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

def get_events():
    sql = """SELECT e.id, e.title, e.content, e.start_time, e.username
             FROM events e
             """
    return db.query(sql)

def get_user_events(username):
    sql = """SELECT e.id, e.title, e.content, e.start_time, e.username
             FROM events e WHERE e.username = ?"""
    return db.query(sql, [username])

def get_user_participations(username):
    sql = """SELECT e.id, e.title, e.content, e.start_time, e.username
             FROM events e
             JOIN event_participants ep ON e.id = ep.event_id
             WHERE ep.username = ?"""
    return db.query(sql, [username])

def search_events(search):
    sql = """SELECT e.id, e.title, e.content, e.start_time, e.username
             FROM events e WHERE e.title LIKE ? OR e.content LIKE ?"""
    return db.query(sql, ["%" + search + "%", "%" + search + "%"])

def get_event(event_id):
    sql = """SELECT e.id, e.title, e.content, e.start_time, e.username
             FROM events e WHERE e.id = ?"""
    return db.query(sql, [event_id])[0]

def update_event(event_id, title, content, start_time):
    sql = """UPDATE events SET title = ?, content = ?, start_time = ? WHERE id = ?"""
    db.execute(sql, [title, content, start_time, event_id])

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

