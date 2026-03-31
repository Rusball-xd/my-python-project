from functions import db
import subprocess
import time
subprocess.run(['python3', 'server.py'])
try:
    db.start_db()
except:
    pass
while True:
    db.deletee(int(time.time()))
    time.sleep(600)
