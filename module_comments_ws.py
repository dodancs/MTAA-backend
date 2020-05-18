from flask import request, jsonify, escape
from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity, get_raw_jwt,
    decode_token
)
from flask_jwt_extended.config import config
from flask_socketio import send, emit
import uuid
import json
import peewee

from helpers import Response, Sanitize
import models

from __main__ import socketio, Config, logger


def verify_token(token):
    token_data = decode_token(token)
    return token_data[config.identity_claim_key]


@socketio.on('connect')
def websocketTest():
    logger.info('CONNECTED')
    emit('my_response', {'data': 'Connected'})


@socketio.on('comment')
def ws_comment_add(data):
    try:
        data['token']
        data['cat']
        data['message']
        if not data['message']:
            raise Exception('message not set')
        models.Cat.get(models.Cat.uuid == data['cat'])
        author = verify_token(data['token'])
        author = models.User.get(models.User.uuid == author)
        comment = models.Comment(
            uuid=uuid.uuid4(), author=author.uuid, cat=data['cat'], text=data['message'])
        comment.save()
        emit('comment', {
            'author': author.getName(),
            'cat': data['cat'],
            'message': data['message'],
        }, broadcast=True)
    except Exception as e:
        print(e)
        pass


@socketio.on('get_comments')
def ws_comments_get(data):
    try:
        data['token']
        data['cat']
        models.Cat.get(models.Cat.uuid == data['cat'])
        author = verify_token(data['token'])
        models.User.get(models.User.uuid == author)
        comments = models.Comment.select().where(
            models.Comment.cat == data['cat'])
        response = []
        for c in comments:
            a = models.User.get(models.User.uuid == c.author)
            response.append({
                'author': a.getName(),
                'message': c.text,
            })
        emit('comments', response)
    except Exception as e:
        print(e)
        emit('comments', [])
        pass


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected', request.sid)
