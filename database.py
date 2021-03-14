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
    conn = sqlite3.connect('Users2.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS Users2(
                username text,
                email text,
                password text
        )""")
    conn.commit()
    conn = sqlite3.connect('garbage.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS garbage(
                    username text,
                    status text,
                    kind text
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

def get_poits(user):
    conn = sqlite3.connect('UserPoints.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS UserPoints(
                username text,
                points text
        )""")
    conn.commit()
    find_user = ("SELECT * FROM UserPoints WHERE username = ?")
    c.execute(find_user, [user])
    result = c.fetchone()
    return result

def insert_points(user, poits):
    conn = sqlite3.connect('UserPoints.db')
    c = conn.cursor()
    c.execute("INSERT INTO UserPoints VALUES (?, ?)",
              (user, poits))
    conn.commit()

def get_status():
    conn = sqlite3.connect('status.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS status(
                    status_code text,
                    id integer
            )""")


    conn.commit()
    c.execute("SELECT * FROM status")
    result = c.fetchone()
    return result

def set_status(status):
    conn = sqlite3.connect('status.db')
    c = conn.cursor()
    if status == 'True':
        c.execute("UPDATE status SET status_code = 'True' WHERE status_code = 'False'")
    if status == 'False':
        c.execute("UPDATE status SET status_code = 'False' WHERE status_code = 'True'")
    conn.commit()




def special_sing_up(email):
    conn = sqlite3.connect('Users2.db')
    c = conn.cursor()
    find_user = ("SELECT * FROM Users2 WHERE email = ?")
    c.execute(find_user, [email])
    result = c.fetchone()
    return result

def special_login_test(email, password):
    conn = sqlite3.connect('Users2.db')
    c = conn.cursor()
    find_user = ("SELECT * FROM Users2 WHERE email = ? AND password = ?")
    c.execute(find_user, [email, password])
    result = c.fetchone()
    return result

def insert_special_user(username, email, password):
    conn = sqlite3.connect('Users2.db')
    c = conn.cursor()
    c.execute("INSERT INTO Users2 VALUES (?, ?, ?)",
              (username, email, password))
    conn.commit()

def get_garbage_info(username):
    conn = sqlite3.connect('garbage.db')
    c = conn.cursor()
    find_user = ("SELECT * FROM garbage WHERE username = ?")
    c.execute(find_user, [username])
    result = c.fetchone()
    if result == None:
        return result
    else:
        return result[1]


def insert_new_garbage(username, kind):
    conn = sqlite3.connect('garbage.db')
    c = conn.cursor()
    status = 'Not Taken'
    c.execute("INSERT INTO garbage VALUES (?, ?, ?)",
              (username, status, kind))
    conn.commit()

def garbage_taken(username):
    conn = sqlite3.connect('garbage.db')
    c = conn.cursor()
    update = ("UPDATE garbage SET status = 'Taken' WHERE username = ?")
    c.execute(update, [username])
    conn.commit()