from flask import Flask, make_response, request, jsonify
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


# if __name__ == '__main__':
#     app.run()
