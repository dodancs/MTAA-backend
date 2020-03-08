from flask import Flask, make_response, request, jsonify
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from flask_socketio import SocketIO, send, emit
import uuid
import json

with open('config.json') as config_file:
    config = json.load(config_file)

app = Flask(__name__)
app.config['SECRET_KEY'] = config['secret']
app.config['JWT_SECRET_KEY'] = config['jwt_secret']
jwt = JWTManager(app)
socketio = SocketIO(app)


@app.route('/')
def hello_world():
    return 'Hello, World!'


# @socketio.on('connect')
# def websocketTest():
#     emit('my response', {'data': 'Connected'})


if __name__ == '__main__':
    socketio.run(app)

# if __name__ == '__main__':
#     app.run()
