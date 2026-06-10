import sqlite3


def start_db():
    db = sqlite3.connect("main.db")
    g = db.cursor()
    g.execute(
        "CREATE TABLE IF NOT EXISTS users(user INTEGER NOT NULL, expiration INTEGER, payment_status INTEGER NOT NULL)")
    db.commit()
    db.close()


def ins(data):
    db = sqlite3.connect("main.db")
    g = db.cursor()
    g.execute("INSERT INTO users(user, expiration, payment_status) VALUES(?, ?, ?)",
              (data[0], data[1], data[2]))
    db.commit()
    db.close()




def change_expiration(user_id, expiration):
    db = sqlite3.connect("main.db")
    g = db.cursor()
    g.execute("UPDATE users SET expiration = ? WHERE user_id = ?", (expiration, user_id))
    db.commit()
    db.close()


def check_for_status(user_id):
    db = sqlite3.connect("main.db")
    g = db.cursor()
    g.execute("SELECT * FROM users WHERE user = ?", (user_id,))

    return g.fetchone()


def change_status(user_id, payment_status):
    db = sqlite3.connect("main.db")
    g = db.cursor()
    g.execute("UPDATE users SET payment_status = ? WHERE user_id = ?", (payment_status, user_id))
    db.commit()
    db.close()

def deletee(data):
    db = sqlite3.connect("main.db")
    g = db.cursor()
    g.execute(f"SELECT * FROM users WHERE expiration <= ?", (data, ))
    k = g.fetchall()
    # создать индекс, то, что сейчас - сильно диск грузит
    g.execute(f"DELETE FROM users WHERE expiration <= ?", (data, ))
    db.commit()
    db.close()


