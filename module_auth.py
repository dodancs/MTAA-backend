from flask import request, jsonify
from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity, get_raw_jwt
)
import uuid
import json
import peewee
import os

from helpers import Response, MakeHash, ConvertImage, Sanitize
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
        return jsonify({'error': 'E-mailová adresa nebola zadaná'}), 400
    if not password:
        return jsonify({'error': 'Heslo nebolo zadané'}), 400

    if not isinstance(email, str) or not isinstance(password, str):
        return Response('invalid_format')

    # Try to get user by provided email
    try:
        match = models.User.get(models.User.email == Sanitize(email))
    except peewee.DoesNotExist:
        return jsonify({'error': 'Používateľ neexistuje'}), 400
    except:
        return Response('server_error')

    if not match.activated:
        return jsonify({'error': 'Účet nie je aktivovaný'}), 400

    # Compare password hashes
    salt = bytes.fromhex(match.password[:(Config['hash_salt_length'] * 2)])
    if match.password == MakeHash(Sanitize(password), salt):
        token = create_access_token(identity=match.uuid)
        return jsonify({
            'token': token,
            'token_type': app.config['JWT_HEADER_TYPE'],
            'expires': Config['jwt_expires'],
            'uuid': match.uuid,
        })
    else:
        return jsonify({'error': 'Nesprávne heslo'}), 400


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
        return jsonify({'error': 'E-mailová adresa nebola zadaná'}), 400
    if not password:
        return jsonify({'error': 'Heslo nebolo zadané'}), 400
    if not firstname:
        return jsonify({'error': 'Meno nebolo zadané'}), 400
    if not lastname:
        return jsonify({'error': 'Priezvisko nebolo zadané'}), 400
    if not picture:
        picture = Config['default_picture']

    if not isinstance(email, str) or not isinstance(password, str):
        return Response('invalid_format')

    try:
        models.Picture.get(models.Picture.uuid == picture)
    except peewee.DoesNotExist:
        return jsonify({'error': 'Obrázok neexistuje'}), 400
    except:
        return Response('server_error')

    hashed_password = MakeHash(
        Sanitize(password), os.urandom(Config['hash_salt_length']))

    user = models.User(uuid=uuid.uuid4(), email=Sanitize(email), password=hashed_password,
                       firstname=Sanitize(firstname), lastname=Sanitize(lastname), picture=picture)

    try:
        user.save()
    except peewee.IntegrityError:
        return jsonify({'error': 'E-mailová adresa už bola použitá'}), 400
    except:
        return Response('server_error')

    seed = os.urandom(128).hex()
    models.Activation(user=user.uuid, seed=seed).save()

    print('Please visit http://127.0.0.1:5000/auth/activate/%s' % seed)

    return Response('empty')


@app.route('/auth/activate/<seed>', methods=['GET'])
def auth_activate(seed):
    try:
        match = models.Activation.get(models.Activation.seed == Sanitize(seed))
        user = models.User.get(models.User.uuid == match.user)
        user.activated = True
        user.save()
        match.delete_instance()
    except peewee.DoesNotExist:
        return Response('empty')
    except:
        return Response('server_error')

    return Response('empty')


@app.route('/auth/refresh_token', methods=['GET'])
@jwt_required
def refresh_token():
    current_user = get_jwt_identity()
    try:
        models.User.get(models.User.uuid == current_user)
    except:
        return Response('forbidden')

    # Add old token to blacklist
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)

    token = create_access_token(identity=current_user)
    return jsonify({
        'token': token,
        'token_type': app.config['JWT_HEADER_TYPE'],
        'expires': Config['jwt_expires'],
        'uuid': current_user,
    })


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
            'uuid': user.uuid,
            'email': user.email,
            'firstname': user.firstname,
            'lastname': user.lastname,
            'activated': True if user.activated else False,
            'admin': True if user.admin else False,
            'created_at': user.created_at.strftime(Config['date_format']),
            'updated_at': user.updated_at.strftime(Config['date_format'])
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

    try:
        match = models.User.get(models.User.uuid == uuid)
    except peewee.DoesNotExist:
        return Response('invalid')
    except:
        return Response('server_error')

    favourites = []
    donations = 0

    try:
        favs = models.Favourite.select().where(models.Favourite.user == user.uuid)
        for f in favs:
            favourites.append(f.cat)
    except:
        pass

    try:
        donats = models.Donation.select().where(models.Donation.donator == user.uuid)
        for d in donats:
            donations += d.amount
    except:
        pass

    if uuid == user.uuid or user.admin:
        return jsonify({
            'uuid': match.uuid,
            'email': match.email,
            'firstname': match.firstname,
            'lastname': match.lastname,
            'activated': True if match.activated else False,
            'admin': True if match.admin else False,
            'donations': donations,
            'picture': match.picture,
            'favourites': favourites,
            'created_at': match.created_at.strftime(Config['date_format']),
            'updated_at': match.updated_at.strftime(Config['date_format'])
        }), 200
    else:
        return jsonify({
            'uuid': match.uuid,
            'firstname': match.firstname,
            'lastname': match.lastname,
            'picture': match.picture
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
        password = request.json.get('password', None)
        firstname = request.json.get('firstname', None)
        lastname = request.json.get('lastname', None)
        picture = request.json.get('picture', None)
        activated = request.json.get('activated', None)
        admin = request.json.get('admin', None)
    except:
        return Response('not_json')

    if not password and not firstname and not lastname and not picture and activated == None and admin == None:
        return Response('empty')

    if admin and not user.admin:
        return Response('forbidden')
    if activated and not user.admin:
        return Response('forbidden')

    if password:
        salt = bytes.fromhex(match.password[:(Config['hash_salt_length'] * 2)])
        match.password = MakeHash(Sanitize(password), salt)
    if firstname:
        match.firstname = Sanitize(firstname)
    if lastname:
        match.lastname = Sanitize(lastname)
    if picture:
        try:
            models.Picture.get(models.Picture.uuid == picture)
        except peewee.DoesNotExist:
            return jsonify({'error': 'Obrázok neexistuje'}), 400
        except:
            return Response('server_error')

        match.picture = picture
    if activated != None:
        match.activated = True if activated else False
    if admin != None:
        match.admin = True if admin else False

    try:
        match.save()
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

    try:
        pictures = models.Picture.select().where(models.Picture.owner == uuid)
        for picture in pictures:
            if picture.uuid == Confg['default_picture']:
                continue
            try:
                os.remove(Config['upload_folder'] +
                          str(picture.uuid) + '.' + Config['image_store_format'])
                picture.delete_instance()
            except:
                pass
    except:
        pass

    try:
        models.Favourite.delete().where(models.Favourite.user == uuid).execute()
    except:
        pass

    try:
        models.Comment.delete().where(models.Comment.author == uuid).execute()
    except:
        pass

    return Response('empty')
