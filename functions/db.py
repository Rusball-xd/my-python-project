import sqlite3
def start_db():
    db = sqlite3.connect("brrbrrpatapim.db")
    g = db.cursor()
    g.execute("CREATE TABLE users(user INTEGER NOT NULL, expiration  INTEGER NOT NULL)")
    db.commit()
    db.close()
def ins(b):
    db = sqlite3.connect("brrbrrpatapim.db")
    g = db.cursor()
    g.execute("INSERT INTO users(user, expiration) VALUES(?, ?)", (b[0], b[1]))
    db.commit()
    db.close()
def deletee(b):
    db = sqlite3.connect("brrbrrpatapim.db")
    g = db.cursor()
    g.execute(f"SELECT * FROM users WHERE expiration <= {b}")
    k = g.fetchall()
    g.execute(f"DELETE FROM users WHERE expiration <= {b}") #создать индекс, то, что сейчас - сильно диск грузит
    db.commit()
    db.close()
def search(b):
    conn = sqlite3.connect("brrbrrpatapim.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user = ?", (b))
    result = cursor.fetchone()
    db.close()
