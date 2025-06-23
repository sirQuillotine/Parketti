import db

def moro():
    print("Moro")

def register_user(username, password_hash):
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])

def get_password_hash(username):
    sql = "SELECT password_hash FROM users WHERE username = ?"
    return db.query(sql, [username])[0][0] if db.query(sql, [username]) else ""