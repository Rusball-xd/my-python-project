from flask import Flask, request, jsonify
import json
import subprocess
app = Flask(__name__)
import logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Удалить пира с ключом
#delete_peer("/etc/amnezia/amneziawg.conf", "xxxxx")
@app.route('/add', methods=['POST'])
def get_data(): #слушает входящие запросы
    data = request.get_json()
    time = data.get("time")
    #написать subprocess.run, который сначала добавляет пользователя сроком на 1 день, потом в /root/awg/etc/<имяпользователя> изменяет время на то, нужно мне
@app.route('/time', methods=['POST'])
def get_data(): #слушает входящие запросы
    data = request.get_json()
    time = data.get("time")
    #написать subprocess.run, который пишет в /root/awg/etc/<имяпользователя> время его окончания+время, на которое он продлил подписку



app.run(host='10.9.0.2', port=5000)
