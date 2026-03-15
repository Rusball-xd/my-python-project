import sqlite3
def start_db():
    db = sqlite3.connect("brrbrrpatapim.db")
    g = db.cursor()
    g.execute("CREATE TABLE users(user TEXT NOT NULL, expiration  INTEGER NOT NULL)")
    db.commit()
    db.close()
def ins(b):
    db = sqlite3.connect("brrbrrpatapim.db")
    g = db.cursor()
    g.execute("INSERT INTO users(user, expiration) VALUES(?, ?)", (b[0], b[1]))
    db.commit()
    db.close()
def del(b)
    db = sqlite3.connect("brrbrrpatapim.db")
    g = db.cursor()
    g.execute(f"DELETE FROM users WHERE expiration <= {b[0]}") #создать индекс, то, что сейчас - сильно диск грузит
    db.commit()
    db.close()
