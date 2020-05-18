from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, get_raw_jwt
from flask_socketio import SocketIO, emit
import json
import logging

from helpers import Response
from models.BaseModel import db

# Open configuration file
with open('config.json', encoding='utf8') as config_file:
    Config = json.load(config_file)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('werkzeug')
print(logger)

# Setup Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = Config['secret']
app.config['JWT_SECRET_KEY'] = Config['jwt_secret']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = Config['jwt_expires']
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']

# Connect to the database before request
@app.before_request
def _db_connect():
    db.connect()


# Disconnect from the database after finishing the request
@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        db.close()


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
# namespace = '/cilicat'


@app.errorhandler(405)
def e495(e):
    return jsonify({'error': 'Metóda nie je podporovaná'}), 405


import module_settings
import module_pictures
import module_cats
import module_auth
# import module_comments
import module_comments_ws
import module_shelterneeds
import module_donations


# @socketio.on('message', namespace=namespace)
# def msg(msg):
#     emit('my_response', msg + 'dasdasdasdadassdasdas')


# @socketio.on('connect')
# def websocketTest():
#     emit('my response', {'data': 'Connected'})
if __name__ == '__main__':
    # if the server runs unreliably, uncomment the first line, and comment the line with socketio
    # app.run(host='0.0.0.0')

    # socketio.init_app(app, cors_allowed_origins="*")
    socketio.run(app, host='0.0.0.0', log=logger, log_output=True,
                 port=5000, use_reloader=False, debug=True)
