from functions import db
#import subprocess
import time
import requests
import json

try:
    db.start_db()
except:
    pass
while True:
    k = db.deletee(int(time.time()))
    k = json.dumps(k)
    response = requests.post('http://10.9.0.1:433/xes', data=k)
    time.sleep(600)
