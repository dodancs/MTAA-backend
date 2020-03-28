from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, get_raw_jwt
from flask_socketio import SocketIO, send, emit
import json

from helpers import Response

# Open configuration file
with open('config.json', encoding='utf8') as config_file:
    Config = json.load(config_file)

# Setup Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = Config['secret']
app.config['JWT_SECRET_KEY'] = Config['jwt_secret']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = Config['jwt_expires']
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']

# Setup JWT
jwt = JWTManager(app)
blacklist = set()
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(token):
    jti = token['jti']
    return jti in blacklist


@jwt.expired_token_loader
def expired_token_callback():
    return Response('forbidden')


@jwt.revoked_token_loader
def revoked_token_callback():
    return Response('forbidden')


@jwt.invalid_token_loader
def invalid_token_callback(reason):
    return Response('forbidden')


@jwt.unauthorized_loader
def unauthorized_token_callback(reason):
    return Response('forbidden')


# Setup SocketIO
socketio = SocketIO(app)


@app.errorhandler(405)
def e495(e):
    return jsonify({'error': 'Metóda nie je podporovaná'}), 405


@app.route('/')
def hello_world():
    return 'Hello, World!'


import module_settings
import module_pictures
import module_cats
import module_auth
import module_comments

# @socketio.on('connect')
# def websocketTest():
#     emit('my response', {'data': 'Connected'})
if __name__ == '__main__':
    # app.run(host='0.0.0.0')
    socketio.run(app, host='0.0.0.0', debug=True)
