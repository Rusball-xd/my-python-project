import sqlite3
db = sqlite3.connect("brrbrrpatapim.db")
g = db.cursor()
g.execute("CREATE TABLE users(user TEXT NOT NULL, expiration  INTEGER NOT NULL)")
db.commit()

b = input()
b = b.split()
print(b)

g.execute("INSERT INTO users(expiration) VALUES(?, ?)", (b[0], b[1]))
