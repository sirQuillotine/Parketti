import db

def register_user(username, password_hash):
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])

def get_password_hash(username):
    sql = "SELECT password_hash FROM users WHERE username = ?"
    return db.query(sql, [username])[0][0] if db.query(sql, [username]) else ""

def update_image(username, image):
    sql = "UPDATE users SET image = ? WHERE username = ?"
    db.execute(sql, [image, username])

def get_image(username):
    sql = "SELECT image FROM users WHERE username = ?"
    return db.query(sql, [username])[0][0] if db.query(sql, [username]) else ""

def has_image(username):
    sql = """SELECT id, username, image IS NOT NULL has_image
             FROM users
             WHERE username = ?"""
    result = db.query(sql, [username])
    return result[0] if result else None