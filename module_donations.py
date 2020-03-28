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


@app.route('/donation', methods=['POST'])
@jwt_required
def donation():
    # get current user
    current_user = get_jwt_identity()
    try:
        # if user does not exist in DB, forbidden
        models.User.get(models.User.uuid == current_user)
    except:
        return Response('forbidden')

    try:
        donator = request.json.get('donator', None)
        amount = request.json.get('amount', None)
    except:
        return Response('not_json')

    if not amount:
        return jsonify({"error": "Suma nebola zadaná"}), 400

    if not isinstance(amount, float) and not isinstance(amount, int):
        return Response('invalid_format')

    if donator:
        try:
            # if user does not exist in DB, error
            models.User.get(models.User.uuid == donator)
        except:
            return jsonify({'error': 'Používateľ neexistuje'}), 400

    donation = models.Donation(donator=Sanitize(donator), amount=amount)

    try:
        donation.save()
    except:
        return Response('server_error')

    return Response('empty')
