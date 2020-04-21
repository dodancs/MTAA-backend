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


@app.route('/settings/colours', methods=['GET'])
def settings_colours_get():
    colours = models.Colour.select()
    response = {}
    response['count'] = len(colours)
    response['colours'] = []
    for c in colours:
        response['colours'].append({
            'id': c.id,
            'name': c.name
        })
    return jsonify(response), 200


@app.route('/settings/colours', methods=['POST'])
@jwt_required
def settings_colours_add():
    current_user = get_jwt_identity()
    try:
        user = models.User.get(models.User.uuid == current_user)
    except:
        return Response('forbidden')
    if not user.admin:
        return Response('forbidden')

    try:
        name = request.json.get('name', None)
    except:
        return Response('not_json')

    if not name:
        return jsonify({'error': 'Žiadna farba nebola zadaná'}), 400

    colour = models.Colour(name=name)

    try:
        colour.save()
    except peewee.IntegrityError:
        return jsonify({'error': 'Farba už existuje'}), 400
    except:
        return Response('server_error')

    return jsonify({'id': colour.id}), 200


@app.route('/settings/colours/<id>', methods=['DELETE'])
@jwt_required
def settings_colours_delete(id):
    current_user = get_jwt_identity()
    try:
        user = models.User.get(models.User.uuid == current_user)
    except:
        return Response('forbidden')
    if not user.admin:
        return Response('forbidden')

    try:
        colour = models.Colour.get(models.Colour.id == id)
    except:
        return Response('empty')

    colour.delete_instance()

    return Response('empty')


@app.route('/settings/breeds', methods=['GET'])
def settings_breeds_get():
    breeds = models.Breed.select()
    response = {}
    response['count'] = len(breeds)
    response['breeds'] = []
    for b in breeds:
        response['breeds'].append({
            'id': b.id,
            'name': b.name
        })
    return jsonify(response), 200


@app.route('/settings/breeds', methods=['POST'])
@jwt_required
def settings_breeds_add():
    current_user = get_jwt_identity()
    try:
        user = models.User.get(models.User.uuid == current_user)
    except:
        return Response('forbidden')
    if not user.admin:
        return Response('forbidden')

    try:
        name = request.json.get('name', None)
    except:
        return Response('not_json')

    if not name:
        return jsonify({'error': 'Žiadne plemeno nebolo zadané'}), 400

    breed = models.Breed(name=name)

    try:
        breed.save()
    except peewee.IntegrityError:
        return jsonify({'error': 'Plemeno už existuje'}), 400
    except:
        return Response('server_error')

    return jsonify({'id': breed.id}), 200


@app.route('/settings/breeds/<id>', methods=['DELETE'])
@jwt_required
def settings_breeds_delete(id):
    current_user = get_jwt_identity()
    try:
        user = models.User.get(models.User.uuid == current_user)
    except:
        return Response('forbidden')
    if not user.admin:
        return Response('forbidden')

    try:
        breed = models.Breed.get(models.Breed.id == id)
    except:
        return Response('empty')

    breed.delete_instance()

    return Response('empty')


@app.route('/settings/health_statuses', methods=['GET'])
def settings_health_statuses_get():
    health_statuses = models.HealthStatus.select()
    response = {}
    response['count'] = len(health_statuses)
    response['health_statuses'] = []
    for h in health_statuses:
        response['health_statuses'].append({
            'id': h.id,
            'name': h.name
        })
    return jsonify(response), 200


@app.route('/settings/health_statuses', methods=['POST'])
@jwt_required
def settings_health_statuses_add():
    current_user = get_jwt_identity()
    try:
        user = models.User.get(models.User.uuid == current_user)
    except:
        return Response('forbidden')
    if not user.admin:
        return Response('forbidden')

    try:
        name = request.json.get('name', None)
    except:
        return Response('not_json')

    if not name:
        return jsonify({'error': 'Žiadny zdravotný stav nebol zadaný'}), 400

    health_status = models.HealthStatus(name=name)

    try:
        health_status.save()
    except peewee.IntegrityError:
        return jsonify({'error': 'Zdravotný stav už existuje'}), 400
    except:
        return Response('server_error')

    return jsonify({'id': health_status.id}), 200


@app.route('/settings/health_statuses/<id>', methods=['DELETE'])
@jwt_required
def settings_health_statuses_delete(id):
    current_user = get_jwt_identity()
    try:
        user = models.User.get(models.User.uuid == current_user)
    except:
        return Response('forbidden')
    if not user.admin:
        return Response('forbidden')

    try:
        health_status = models.HealthStatus.get(models.HealthStatus.id == id)
    except:
        return Response('empty')

    health_status.delete_instance()

    return Response('empty')
