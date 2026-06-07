import logging
from flask import Flask, request, jsonify
import json
import subprocess
import time
app = Flask(__name__)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Удалить пира с ключом
# delete_peer("/etc/amnezia/amneziawg.conf", "xxxxx")


@app.route('/add', methods=['POST'])
def get_data():  # слушает входящие запросы
    data = request.get_json()
    time = data.get("time")
    user_id = data.get("user_id")
    subprocess.run([
                "/root/awg/manage_amneziawg.sh",
                "add",
                str(user_id),
                "--expires=1d"
            ])
    with open(f'/root/awg/expiry/{user_id}', 'w', encoding='utf-8') as f:
        f.write(str(time))
    with open(f'/root/awg/{user_id}.vpnuri', 'r', encoding='utf-8') as f:
        vpnuri=f.read()
    with open(f'/root/awg/{user_id}.conf', 'r', encoding='utf-8') as f:
        conf=f.read()

    result={
        "vpnuri": vpnuri,
        "conf": conf
        }

    return jsonify(result), 200



app.run(host='10.9.0.1', port=5000)
