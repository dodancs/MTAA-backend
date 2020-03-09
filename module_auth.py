from flask import request, jsonify, escape
from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity, get_raw_jwt
)
import uuid
import json
import peewee
import os

from helpers import Response, MakeHash, ConvertImage
import models

from __main__ import app, Config, blacklist


@app.route('/auth/login', methods=['POST'])
def auth_login():
    if not request.is_json:
        return Response('not_json')

    try:
        email = request.json.get('email', None)
        password = request.json.get('password', None)
    except:
        return Response('not_json')

    if not email:
        return jsonify({"error": "E-mailová adresa nebola zadaná"}), 400
    if not password:
        return jsonify({"error": "Heslo nebolo zadané"}), 400

    # Try to get user by provided email
    try:
        match = models.User.get(models.User.email ==
                                str(escape(email)).strip())
    except peewee.DoesNotExist:
        return jsonify({"error": "Používateľ neexistuje"}), 400
    except:
        return Response('server_error')

    if not match.activated:
        return jsonify({"error": "Účet nie je aktivovaný"}), 400

    # Compare password hashes
    salt = bytes.fromhex(match.password[:(Config['hash_salt_length']*2)])
    if match.password == MakeHash(str(escape(password)).strip(), salt):
        token = create_access_token(identity=match.uuid)
        return jsonify({
            "token": token,
            "token_type": app.config['JWT_HEADER_TYPE'],
            "expires": Config['jwt_expires'],
            "uuid": match.uuid,
            "admin": True if match.admin else False
        })
    else:
        return jsonify({"error": "Nesprávne heslo"}), 400


@app.route('/auth/logout', methods=['GET'])
@jwt_required
def auth_logout():
    # Add token to blacklist
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return Response('empty')


@app.route('/auth/register', methods=['POST'])
def auth_register():
    if not request.is_json:
        return Response('not_json')

    try:
        email = request.json.get('email', None)
        password = request.json.get('password', None)
        firstname = request.json.get('firstname', None)
        lastname = request.json.get('lastname', None)
        picture = request.json.get('picture', None)
    except:
        return Response('not_json')

    if not email:
        return jsonify({"error": "E-mailová adresa nebola zadaná"}), 400
    if not password:
        return jsonify({"error": "Heslo nebolo zadané"}), 400
    if not firstname:
        return jsonify({"error": "Meno nebolo zadané"}), 400
    if not lastname:
        return jsonify({"error": "Priezvisko nebolo zadané"}), 400
    if not picture:
        picture = Config['default_picture']

    picture = str(escape(picture)).strip()
    result = ConvertImage(picture)

    if not result:
        return Response('invalid_image')

    hashed_password = MakeHash(
        str(escape(password)).strip(), os.urandom(Config['hash_salt_length']))

    iid = uuid.uuid4()

    user = models.User(uuid=iid, email=str(escape(email)).strip(), password=hashed_password,
                       firstname=str(escape(firstname)).strip(), lastname=str(escape(lastname)).strip(), picture=result)

    try:
        user.save()
    except peewee.IntegrityError:
        return jsonify({"error": "E-mailová adresa už bola použitá"}), 400
    except:
        return Response('server_error')

    seed = os.urandom(128).hex()
    models.Activation(user=iid, seed=seed).save()

    print('Please visit http://127.0.0.1:5000/auth/activate/%s' % seed)

    return Response('empty')


@app.route('/auth/activate/<seed>', methods=['GET'])
def auth_activate(seed):
    try:
        match = models.Activation.get(models.Activation.seed ==
                                      str(escape(seed)).strip())
        user = models.User.get(models.User.uuid == match.user)
        user.activated = True
        user.save()
        match.delete_instance()
    except peewee.DoesNotExist:
        return Response('empty')
    except:
        return Response('server_error')

    return Response('empty')


@app.route('/auth/users', methods=['GET'])
@jwt_required
def auth_get_users():
    current_user = get_jwt_identity()
    try:
        user = models.User.get(models.User.uuid == current_user)
    except:
        return Response('forbidden')

    if not user.admin:
        return Response('forbidden')

    query = models.User.select()
    response = {}
    response['count'] = len(query)
    response['users'] = []
    for user in query:
        response['users'].append({
            "uuid": user.uuid,
            "email": user.email,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "activated": True if user.activated else False,
            "admin": True if user.admin else False,
            "created_at": user.created_at.strftime(Config['date_format']),
            "updated_at": user.updated_at.strftime(Config['date_format'])
        })
    return jsonify(response), 200


@app.route('/auth/users/<uuid>', methods=['GET'])
@jwt_required
def auth_get_user(uuid):
    current_user = get_jwt_identity()
    try:
        user = models.User.get(models.User.uuid == current_user)
    except:
        return Response('forbidden')
    if uuid != user.uuid and not user.admin:
        return Response('forbidden')

    try:
        match = models.User.get(models.User.uuid == uuid)
    except peewee.DoesNotExist:
        return Response('invalid')
    except:
        return Response('server_error')

    return jsonify({
        "uuid": match.uuid,
        "email": match.email,
        "firstname": match.firstname,
        "lastname": match.lastname,
        "activated": True if match.activated else False,
        "admin": True if match.admin else False,
        "donations": match.donations,
        "picture": match.picture,
        "created_at": match.created_at.strftime(Config['date_format']),
        "updated_at": match.updated_at.strftime(Config['date_format'])
    }), 200


@app.route('/auth/users/<uuid>', methods=['PUT'])
@jwt_required
def auth_update_user(uuid):
    current_user = get_jwt_identity()
    try:
        user = models.User.get(models.User.uuid == current_user)
    except:
        return Response('forbidden')
    if uuid != user.uuid and not user.admin:
        return Response('forbidden')

    try:
        match = models.User.get(models.User.uuid == uuid)
    except peewee.DoesNotExist:
        return Response('invalid')
    except:
        return Response('server_error')

    if not request.is_json:
        return Response('not_json')

    try:
        email = request.json.get('email', None)
        password = request.json.get('password', None)
        firstname = request.json.get('firstname', None)
        lastname = request.json.get('lastname', None)
        picture = request.json.get('picture', None)
        activated = request.json.get('activated', None)
        admin = request.json.get('admin', None)
    except:
        return Response('not_json')

    if not email and not password and not firstname and not lastname and not picture and not activated and not admin:
        return Response('empty')

    if admin and not user.admin:
        return Response('forbidden')
    if activated and not user.admin:
        return Response('forbidden')

    if email:
        match.email = str(escape(email)).strip()
    if password:
        salt = bytes.fromhex(match.password[:(Config['hash_salt_length']*2)])
        match.password = MakeHash(str(escape(password)).strip(), salt)
    if firstname:
        match.firstname = str(escape(firstname)).strip()
    if lastname:
        match.lastname = str(escape(lastname)).strip()
    if picture:
        picture = str(escape(picture)).strip()
        result = ConvertImage(picture)

        if not result:
            return Response('invalid_image')

        match.picture = result
    if activated:
        match.activated = True if activated else False
    if admin:
        match.admin = True if admin else False

    try:
        match.save()
    except peewee.IntegrityError:
        return jsonify({"error": "E-mailová adresa už bola použitá"}), 400
    except:
        return Response('server_error')

    return Response('empty')


@app.route('/auth/users/<uuid>', methods=['DELETE'])
@jwt_required
def auth_delete_user(uuid):
    current_user = get_jwt_identity()
    try:
        user = models.User.get(models.User.uuid == current_user)
    except:
        return Response('forbidden')
    if uuid != user.uuid and not user.admin:
        return Response('forbidden')

    try:
        match = models.User.get(models.User.uuid == uuid)
        activations = models.Activation.select().where(
            models.Activation.user == match.uuid)
    except peewee.DoesNotExist:
        return Response('invalid')
    except:
        return Response('server_error')

    match.delete_instance()
    for a in activations:
        a.delete_instance()

    if uuid == user.uuid:
        blacklist.add(get_raw_jwt()['jti'])

    return Response('empty')
