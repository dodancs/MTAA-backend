from flask import request, jsonify, escape
from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity, get_raw_jwt
)
import uuid
import json
import peewee

from helpers import Response, Sanitize
import models

from __main__ import app, Config


@app.route('/comments/<uuid>', methods=['GET'])
@jwt_required
def comments_get(uuid):
    # get current user
    current_user = get_jwt_identity()
    try:
        # if user does not exist in DB, forbidden
        models.User.get(models.User.uuid == current_user)
    except:
        return Response('forbidden')

    try:
        models.Cat.get(models.Cat.uuid == uuid)
    except peewee.DoesNotExist:
        return Response('invalid')
    except:
        return Response('server_error')

    comments = models.Comment.select().where(models.Comment.cat == uuid)

    response = {}
    response['count'] = len(comments)
    response['comments'] = []
    for comment in comments:
        response['comments'].append({
            "uuid": comment.uuid,
            "author": comment.author,
            "cat": comment.cat,
            "text": comment.text,
            "created_at": comment.created_at.strftime(Config['date_format'])
        })
    return jsonify(response), 200


@app.route('/comments/<u>', methods=['POST'])
@jwt_required
def comments_add(u):
    # get current user
    current_user = get_jwt_identity()
    try:
        # if user does not exist in DB, forbidden
        user = models.User.get(models.User.uuid == current_user)
    except:
        return Response('forbidden')

    try:
        models.Cat.get(models.Cat.uuid == u)
    except peewee.DoesNotExist:
        return Response('invalid')
    except:
        return Response('server_error')

    try:
        text = request.json.get('text', None)
    except:
        return Response('not_json')

    if not text:
        return jsonify({"error": "Komentár nebol zadaný"}), 400

    comment = models.Comment(
        uuid=uuid.uuid4(), author=user.uuid, cat=u, text=Sanitize(text))

    try:
        comment.save()
    except:
        return Response('server_error')

    return Response('empty')


@app.route('/comments/<uuid>', methods=['DELETE'])
@jwt_required
def comments_delete(uuid):
    # get current user
    current_user = get_jwt_identity()
    try:
        # if user does not exist in DB, forbidden
        user = models.User.get(models.User.uuid == current_user)
    except:
        return Response('forbidden')

    try:
        comment = models.Comment.get(models.Comment.uuid == uuid)
    except peewee.DoesNotExist:
        return Response('invalid')
    except:
        return Response('server_error')

    if comment.author != user.uuid and not user.admin:
        return Response('forbidden')

    comment.delete_instance()

    return Response('empty')
