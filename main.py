from functions import db
import subprocess
import time
import requests
import json
try:
    db.start_db()
except:
    pass
subprocess.run(["python3", "bot.py"])
while True:
    k = db.deletee(int(time.time()))
    k = json.dumps(k)
    print(k)
    time.sleep(600)
