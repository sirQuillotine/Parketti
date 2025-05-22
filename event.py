import db

def add_event(title, content, start_time, username):
    sql = "INSERT INTO events (title, content, start_time, username) VALUES (?, ?, ?, ?)"
    db.execute(sql, [title, content, start_time, username])
    event_id = db.last_insert_id()
    return event_id

def get_events():
    sql = """SELECT e.id, e.title, e.content, e.start_time, e.username
             FROM events e
             """
    return db.query(sql)

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

