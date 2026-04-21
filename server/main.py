from flask import Flask, request, jsonify
import json
import subprocess
app = Flask(__name__)
import logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

@app.route('/xes', methods=['POST'])
def post_data(): #слушает входящие запросы
    data = request.get_json()
    data = data.get("users", [])
    for i in data:
        subprocess.run("docker", "exec", "amnezia-awg2", "awg", "set", "wg0", "peer", f"{i[0]}", "remove")
    logging.info(f"accepted request for deleting {len(data)} users")
    return 202
    #сервер периодически хавает запросы на удаление пользователей от СУБД
app.run(host='10.9.0.2', port=5000)
