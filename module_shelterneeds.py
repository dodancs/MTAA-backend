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


@app.route('/shelterneeds', methods=['GET'])
@jwt_required
def shelterneeds_get():
    # get current user
    current_user = get_jwt_identity()
    try:
        # if user does not exist in DB, forbidden
        user = models.User.get(models.User.uuid == current_user)
    except:
        return Response('forbidden')

    if user.admin:
        shelterneeds = models.ShelterNeeds.select()
    else:
        shelterneeds = models.ShelterNeeds.select().where(
            models.ShelterNeeds.hide == False)

    response = {}
    response['count'] = len(shelterneeds)
    response['shelterneeds'] = []
    for need in shelterneeds:
        response['shelterneeds'].append({
            "uuid": need.uuid,
            "category": need.category,
            "name": need.name,
            "details": need.details,
            "hide": True if need.hide else False
        })
    return jsonify(response), 200


@app.route('/shelterneeds', methods=['POST'])
@jwt_required
def shelterneeds_add():
    # get current user
    current_user = get_jwt_identity()
    try:
        # if user does not exist in DB, forbidden
        user = models.User.get(models.User.uuid == current_user)
    except:
        return Response('forbidden')

    if not user.admin:
        return Response('forbidden')

    try:
        category = request.json.get('category', None)
        name = request.json.get('name', None)
        details = request.json.get('details', None)
        hide = request.json.get('hide', None)
    except:
        return Response('not_json')

    if not category:
        return jsonify({"error": "Kategória nebola zadaná"}), 400

    if not name:
        return jsonify({"error": "Názov nebol zadaný"}), 400

    if not details:
        return jsonify({"error": "Detailný popis nebol zadaný"}), 400

    if not hide:
        hide = False

    shelterneed = models.ShelterNeeds(
        uuid=uuid.uuid4(), category=Sanitize(category), name=Sanitize(name), details=Sanitize(details), hide=hide)

    try:
        shelterneed.save()
    except:
        return Response('server_error')

    return Response('empty')


@app.route('/shelterneeds/<uuid>', methods=['POST'])
@jwt_required
def shelterneeds_toggle(uuid):
    # get current user
    current_user = get_jwt_identity()
    try:
        # if user does not exist in DB, forbidden
        user = models.User.get(models.User.uuid == current_user)
    except:
        return Response('forbidden')

    if not user.admin:
        return Response('forbidden')

    try:
        match = models.ShelterNeeds.get(models.ShelterNeeds.uuid == uuid)
    except peewee.DoesNotExist:
        return Response('invalid')
    except:
        return Response('server_error')

    if match.hide:
        match.hide = False
    else:
        match.hide = True

    try:
        match.save()
    except:
        return Response('server_error')

    return Response('empty')


@app.route('/shelterneeds/<uuid>', methods=['DELETE'])
@jwt_required
def shelterneeds_delete(uuid):
    # get current user
    current_user = get_jwt_identity()
    try:
        # if user does not exist in DB, forbidden
        user = models.User.get(models.User.uuid == current_user)
    except:
        return Response('forbidden')

    if not user.admin:
        return Response('forbidden')

    try:
        shelterneed = models.ShelterNeeds.get(models.ShelterNeeds.uuid == uuid)
    except peewee.DoesNotExist:
        return Response('invalid')
    except:
        return Response('server_error')

    shelterneed.delete_instance()

    return Response('empty')
