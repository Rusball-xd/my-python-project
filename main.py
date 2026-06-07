import db
import subprocess
import time
import json


db.start_db()
subprocess.run(["python3", "bot.py"])
while True:
    try:
        k= db.deletee(int(time.time()))
    except:
        pass
    time.sleep(600)
