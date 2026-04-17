from flask import Flask, request, jsonify


app = Flask(__name__)

@app.route('/xes', methods=['POST'])
def post_data(): #слушает входящие запросы
    data = request.get_json()
    #сервер периодически хавает запросы на удаление пользователей от СУБД
