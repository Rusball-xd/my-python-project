from flask import Flask, request, jsonify
import json
import subprocess
app = Flask(__name__)

@app.route('/xes', methods=['POST'])
def post_data(): #слушает входящие запросы
    data = request.get_json()
    data = json.dumps(data)
    for i in data:
        subprocess.run("docker", "exec", "amnezia-awg2", "awg", "set", "wg0", "peer", f"{i[0]}", "remove")
    #сервер периодически хавает запросы на удаление пользователей от СУБД
