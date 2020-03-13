from flask import request, jsonify, escape, send_file
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


@app.route('/pictures/<uuid>', methods=['GET'])
@jwt_required
def pictures_get(uuid):
    current_user = get_jwt_identity()
    try:
        models.User.get(models.User.uuid == current_user)
    except:
        return Response('forbidden')

    try:
        models.Picture.get(models.Picture.uuid == uuid)
    except peewee.DoesNotExist:
        return Response('invalid')
    except:
        return Response('server_error')

    return send_file(Config['upload_folder'] + uuid + '.' + Config['image_store_format'], mimetype='image/png')


@app.route('/pictures', methods=['POST'])
@jwt_required
def pictures_add():
    current_user = get_jwt_identity()
    try:
        user = models.User.get(models.User.uuid == current_user)
    except:
        return Response('forbidden')

    if not 'image/' in request.headers.get('Content-type'):
        return Response('invalid_format')

    image = ConvertImage(request.get_data(),
                         Config['picture_width'], Config['picture_height'])

    if not image:
        return Response('invalid_image')

    try:
        picture = models.Picture(uuid=uuid.uuid4(), owner=user.uuid)
        picture.save()
    except:
        return Response('server_error')

    fullpath = Config['upload_folder'] + \
        str(picture.uuid) + '.' + Config['image_store_format']

    if not os.path.exists(Config['upload_folder']):
        if Config['debug']:
            print('Debug: Creating leading directories for: %s' %
                  Config['upload_folder'])
        os.makedirs(Config['upload_folder'])

    try:
        if Config['debug']:
            print('Debug: Storing image into: %s' % fullpath)
        with open(fullpath, 'wb+') as f:
            f.write(image.getbuffer())
            f.close()
    except:
        return Response('server_error')

    return jsonify({'uuid': picture.uuid}), 200


@app.route('/pictures/<uuid>', methods=['DELETE'])
@jwt_required
def pictures_delete(uuid):
    current_user = get_jwt_identity()
    try:
        user = models.User.get(models.User.uuid == current_user)
    except:
        return Response('forbidden')

    try:
        picture = models.Picture.get(models.Picture.uuid == uuid)
    except peewee.DoesNotExist:
        return Response('invalid')
    except:
        return Response('server_error')

    if not user.admin and not picture.owner == user.uuid:
        return Response('forbidden')

    fullpath = Config['upload_folder'] + \
        str(picture.uuid) + '.' + Config['image_store_format']

    if os.path.exists(fullpath):
        os.remove(fullpath)

    picture.delete_instance()

    return Response('empty')
