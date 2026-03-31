
from functions import db
from flask import Flask, request, jsonify


app = Flask(__name__)

@app.route('/xes', methods=['POST'])
def post_data(): #слушает входящие запросы
    data = request.get_json()
    db.ins([data.get('user'), data.get('expiration')])
    return 202



