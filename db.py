import sqlite3


def start_db():
    db = sqlite3.connect("brrbrrpatapim.db")
    g = db.cursor()
    g.execute(
        "CREATE TABLE IF NOT EXISTS users(user INTEGER NOT NULL, expiration INTEGER NOT NULL)")
    db.commit()
    db.close()


def ins(data):
    db = sqlite3.connect("brrbrrpatapim.db")
    g = db.cursor()
    g.execute("INSERT INTO users(user, expiration) VALUES(?, ?)",
              (data[0], data[1]))
    db.commit()
    db.close()


def deletee(data):
    db = sqlite3.connect("brrbrrpatapim.db")
    g = db.cursor()
    g.execute(f"SELECT * FROM users WHERE expiration <= ?", (data, ))
    k = g.fetchall()
    # создать индекс, то, что сейчас - сильно диск грузит
    g.execute(f"DELETE FROM users WHERE expiration <= ?", (data, ))
    db.commit()
    db.close()


def search(data):
    conn = sqlite3.connect("brrbrrpatapim.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user = ?", (data,))
    result = cursor.fetchone()
    conn.close()
    return result
