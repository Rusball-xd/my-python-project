from flask import Flask, request, jsonify
import json
import subprocess
app = Flask(__name__)
import logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
def add_peer_to_config(filename, peer_key, allowed_ip):
    with open(filename, "a") as f:
        #f.write(f"\n# Added by bot\n")  # Комментарий, чтобы знать
        f.write(f"[Peer]\n")
        f.write(f"PublicKey = {peer_key}\n")
        f.write(f"AllowedIPs = {allowed_ip}/32\n")
def delete_peer(filename, peer_key):
    with open(filename, "r") as f:
        lines = f.readlines()

    result = []
    skip = False

    for line in lines:
        if f"PublicKey = {peer_key}" in line:
            # Начинаем пропускать этот блок [Peer]
            skip = True
            # Убираем предыдущую строку с [Peer]
            if result and "[Peer]" in result[-1]:
                result.pop()
            continue

        if skip and line.strip() == "":
            skip = False
            continue

        if not skip:
            result.append(line)

    with open(filename, "w") as f:
        f.writelines(result)

# Удалить пира с ключом
#delete_peer("/etc/amnezia/amneziawg.conf", "xxxxx")
@app.route('/add', methods=['POST'])
def post_data(): #слушает входящие запросы
    data = request.get_json()
    data = data.get("users", [])
    for i in data:
        delete_peer("/root/awg0.conf", i)
    subprocess.run("docker", "cp", "/root/awg.conf", "amnezia-awg2:/opt/amnezia/awg/awg0.conf")
    logging.info(f"accepted request for adding {len(data)} users")
    return 202
    #сервер периодически хавает запросы на удаление пользователей от СУБД
@app.route('/del', methods=['POST'])
def get_data():
    data=request.get_json()
    g = data.get("pubkeys", [])
    data = data.get("users", [])
    for i in g:

    logging.info(f"accepted request for deleting {len(data)} users")
    return 202
app.run(host='10.9.0.2', port=5000)
