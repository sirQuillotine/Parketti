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