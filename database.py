import sqlite3

def create_database():
    conn = sqlite3.connect('UsersTry.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS UsersTry(
            username text,
            email text,
            password text
    )""")
    conn.commit()

def singup_test(email):
    conn = sqlite3.connect('UsersTry.db')
    c = conn.cursor()
    find_user = ("SELECT * FROM UsersTry WHERE email = ?")
    c.execute(find_user, [email])
    result = c.fetchone()
    return result

def insert_user(username, email, password):
    conn = sqlite3.connect('UsersTry.db')
    c = conn.cursor()
    c.execute("INSERT INTO UsersTry VALUES (?, ?, ?)",
              (username, email, password))
    conn.commit()

def login_test(email, password):
    conn = sqlite3.connect('UsersTry.db')
    c = conn.cursor()
    find_user = ("SELECT * FROM UsersTry WHERE email = ? AND password = ?")
    c.execute(find_user, [email, password])
    result = c.fetchone()
    return result
