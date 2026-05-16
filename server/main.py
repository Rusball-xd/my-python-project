import logging
import os
import re
import subprocess
from flask import Flask, jsonify, request

app = Flask(__name__)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

BASE_AWG_DIR = "/root/awg"
EXPIRY_DIR = os.path.join(BASE_AWG_DIR, "expiry")
MANAGE_SCRIPT = os.path.join(BASE_AWG_DIR, "manage_amneziawg.sh")


def is_valid_username(username: str) -> bool:
    if not username or not isinstance(username, str):
        return False
    return bool(re.match(r"^[a-zA-Z0-9_\-]+$", username))


@app.route('/add', methods=['POST'])
<<<<<<< HEAD
def handle_add_user():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON payload"}), 400

    expiration_time = data.get("time")
    user_id = data.get("user_id")

    if expiration_time is None or user_id is None:
        return jsonify({"error": "Missing required fields: 'time' and 'user_id'"}), 400

    user_str = str(user_id).strip()
    if not is_valid_username(user_str):
        return jsonify({"error": "Invalid user_id format"}), 400

    try:
        creation_result = subprocess.run(
            [MANAGE_SCRIPT, "add", user_str, "--expires=1d"],
            capture_output=True,
            text=True,
            check=True,
            timeout=15
        )
        logging.info("User creation script output: %s", creation_result.stdout)
    except subprocess.CalledProcessError as err:
        logging.error("Failed to execute creation script: %s", err.stderr)
        return jsonify({"error": "Internal script execution failed"}), 500
    except subprocess.TimeoutExpired:
        logging.error("User creation script timed out")
        return jsonify({"error": "Script execution timed out"}), 504

    try:
        os.makedirs(EXPIRY_DIR, exist_ok=True)
        expiry_file_path = os.path.join(EXPIRY_DIR, user_str)
        with open(expiry_file_path, "w", encoding="utf-8") as expiry_file:
            expiry_file.write(f"{expiration_time}\n")
    except IOError as err:
        logging.error("Failed to write expiry file for user %s: %s", user_str, err)
        return jsonify({"error": "Failed to save expiration data"}), 500

    vpnuri_path = os.path.join(BASE_AWG_DIR, f"{user_str}.vpnuri")
    conf_path = os.path.join(BASE_AWG_DIR, f"{user_str}.conf")

    try:
        with open(vpnuri_path, "r", encoding="utf-8") as file:
            vpn_uri = file.read().strip()
        with open(conf_path, "r", encoding="utf-8") as file:
            vpn_conf = file.read().strip()
    except FileNotFoundError as err:
        logging.error("Generated configuration files not found for user %s: %s", user_str, err)
        return jsonify({"error": "Configuration files were not generated"}), 500
    except IOError as err:
        logging.error("Failed to read configuration files for user %s: %s", user_str, err)
        return jsonify({"error": "Failed to read configuration data"}), 500

    return jsonify({
        "vpnuri": vpn_uri,
        "conf": vpn_conf
    }), 200
=======
def get_data(): #слушает входящие запросы
    data = request.get_json()
    time = data.get("time")
    user_id=data.get("user_id")
    subprocess.run(
            [
                "/root/awg/manage_amneziawg.sh",
                "add",
                str(user_id),
                "--expires=1d"
            ])
    #написать subprocess.run, который сначала добавляет пользователя сроком на 1 день, потом в /root/awg/expiry/<имяпользователя> изменяет время на то, нужно мне
    subprocess.run(f"echo \"{time}\" > /root/awg/expiry/{user_id}", shell=True)
    with open(f'/root/awg/{user_id}.vpnuri', 'r', encoding='utf-8') as f:
        vpnuri = f.read()
    with open(f'/root/awg/{user_id}.conf', 'r', encoding='utf-8') as f:
        conf = f.read()
>>>>>>> test


<<<<<<< HEAD
@app.route('/ping', methods=['GET'])
def handle_ping():
=======
    return jsonify(result), 200
@app.route('/ping', methods=['GET'])
def pinging():
>>>>>>> test
    return "1488", 200


if __name__ == '__main__':
    app.run(host='10.9.0.1', port=5000)
