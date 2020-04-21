from flask import request, jsonify, escape
from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity, get_raw_jwt
)
import operator
from functools import reduce
import uuid
import json
import peewee
import os

from helpers import Response, ConvertImage, Sanitize
import models

from __main__ import app, Config, blacklist


@app.route('/cats', methods=['GET'])
@jwt_required
def cats_get_all():
    # get current user
    current_user = get_jwt_identity()
    try:
        # if user does not exist in DB, forbidden
        models.User.get(models.User.uuid == current_user)
    except:
        return Response('forbidden')

    # default values for page size and current page
    limit = 5
    page = 1

    # dictionary for filters + default values
    f = dict()
    f['adoptive'] = None
    f['sex'] = None
    f['breed'] = None
    f['health_status'] = None
    f['age_up'] = None
    f['age_down'] = None
    f['colour'] = None
    f['castrated'] = None
    f['vaccinated'] = None
    f['dewormed'] = None

    # if limit is specified
    if 'limit' in request.args.keys():
        try:
            limit = int(request.args.get('limit'))
        except:
            return Response('invalid_args')
    # if current page is specified
    if 'page' in request.args.keys():
        try:
            page = int(request.args.get('page'))
        except:
            return Response('invalid_args')

    # if page is zero or less, turn it into a one
    if page < 1:
        page = 1

    # if adoptive is specified
    if 'adoptive' in request.args.keys():
        if str(request.args.get('adoptive')) not in ('true', 'false', 'null'):
            return Response('invalid_args')
        f['adoptive'] = True if str(
            request.args.get('adoptive')) == 'true' else False if str(
            request.args.get('adoptive')) == 'false' else None

    # if sex is specified
    if 'sex' in request.args.keys():
        if str(request.args.get('sex')) not in ('true', 'false', 'null'):
            return Response('invalid_args')
        f['sex'] = True if str(request.args.get('sex')) == 'true' else False if str(
            request.args.get('sex')) == 'false' else None

    # if breed is specified
    if 'breed' in request.args.keys():
        if str(request.args.get('breed')) != 'null':
            try:
                f['breed'] = int(request.args.get('breed'))
            except:
                return Response('invalid_args')
            try:
                models.Breed.get(models.Breed.id == f['breed'])
            except:
                return Response('invalid_args')

    # if health status is specified
    if 'health_status' in request.args.keys():
        if str(request.args.get('health_status')) != 'null':
            try:
                f['health_status'] = int(request.args.get('health_status'))
            except:
                return Response('invalid_args')
            try:
                models.HealthStatus.get(
                    models.HealthStatus.id == f['health_status'])
            except:
                return Response('invalid_args')

    # if age upper limit is specified
    if 'age_up' in request.args.keys():
        if str(request.args.get('age_up')) != 'null':
            try:
                f['age_up'] = int(request.args.get('age_up'))
            except:
                return Response('invalid_args')

    # if age lower limit is specified
    if 'age_down' in request.args.keys():
        if str(request.args.get('age_down')) != 'null':
            try:
                f['age_down'] = int(request.args.get('age_down'))
            except:
                return Response('invalid_args')

    # if colour is specified
    if 'colour' in request.args.keys():
        if str(request.args.get('colour')) != 'null':
            try:
                f['colour'] = int(request.args.get('colour'))
            except:
                return Response('invalid_args')
            try:
                models.Colour.get(
                    models.Colour.id == f['colour'])
            except:
                return Response('invalid_args')

    # if castration is specified
    if 'castrated' in request.args.keys():
        if str(request.args.get('castrated')) not in ('true', 'false', 'null'):
            return Response('invalid_args')
        f['castrated'] = True if str(request.args.get(
            'castrated')) == 'true' else False if str(
            request.args.get('castrated')) == 'false' else None

    # if vaccination is specified
    if 'vaccinated' in request.args.keys():
        if str(request.args.get('vaccinated')) not in ('true', 'false', 'null'):
            return Response('invalid_args')
        f['vaccinated'] = True if str(request.args.get(
            'vaccinated')) == 'true' else False if str(
            request.args.get('vaccinated')) == 'false' else None

    # if dewormation is specified
    if 'dewormed' in request.args.keys():
        if str(request.args.get('dewormed')) not in ('true', 'false', 'null'):
            return Response('invalid_args')
        f['dewormed'] = True if str(request.args.get(
            'dewormed')) == 'true' else False if str(
            request.args.get('dewormed')) == 'false' else None

    # building the query condition list
    expr_list = []
    for key in f.keys():
        if f[key] is not None:
            if key == 'adoptive' and f[key]:
                expr_list.append(models.Cat.adoptive == f[key])
            if key == 'sex':
                expr_list.append(models.Cat.sex == f[key])
            if key == 'breed':
                expr_list.append(models.Cat.breed == f[key])
            if key == 'health_status':
                expr_list.append(models.Cat.health_status == f[key])
            if key == 'age_up':
                expr_list.append(models.Cat.age <= f[key])
            if key == 'age_down':
                expr_list.append(models.Cat.age >= f[key])
            if key == 'colour':
                expr_list.append(models.Cat.colour == f[key])
            if key == 'castrated':
                expr_list.append(models.Cat.castrated == f[key])
            if key == 'vaccinated':
                expr_list.append(models.Cat.vaccinated == f[key])
            if key == 'dewormed':
                expr_list.append(models.Cat.dewormed == f[key])

    allCats = models.Cat.select()
    # if any filters were set, use the where query
    query = allCats.where(reduce(operator.and_, expr_list)
                          ).paginate(page, paginate_by=limit) if expr_list else allCats.paginate(page, paginate_by=limit)
    response = {}
    response['total'] = len(allCats)
    response['count'] = len(query)
    response['page'] = int(page)
    response['cats'] = []
    for cat in query:

        comments = 0
        try:
            comments = len(models.Comment.select().where(
                models.Comment.cat == cat.uuid))
        except:
            pass

        response['cats'].append({
            "uuid": cat.uuid,
            "name": cat.name,
            "age": cat.age,
            "sex": True if cat.sex else False,
            "breed": cat.breed,
            "health_status": cat.health_status,
            "castrated": True if cat.castrated else False,
            "vaccinated": True if cat.vaccinated else False,
            "dewormed": True if cat.dewormed else False,
            "colour": cat.colour,
            "description": cat.description,
            "health_log": cat.health_log,
            "adoptive": True if cat.adoptive else False,
            "pictures": json.loads(cat.pictures),
            "comments": comments,
            "created_at": cat.created_at.strftime(Config['date_format']),
            "updated_at": cat.updated_at.strftime(Config['date_format'])
        })
    return jsonify(response), 200


@app.route('/cats', methods=['POST'])
@jwt_required
def cats_add():
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
        name = request.json.get('name', None)
        age = request.json.get('age', None)
        sex = request.json.get('sex', None)
        breed = request.json.get('breed', None)
        health_status = request.json.get('health_status', None)
        castrated = request.json.get('castrated', None)
        vaccinated = request.json.get('vaccinated', None)
        dewormed = request.json.get('dewormed', None)
        colour = request.json.get('colour', None)
        description = request.json.get('description', None)
        health_log = request.json.get('health_log', '')
        adoptive = request.json.get('adoptive', None)
        pictures = request.json.get('pictures', None)
    except:
        return Response('not_json')

    if not name:
        return jsonify({"error": "Meno nebolo zadané"}), 400
    if not age:
        return jsonify({"error": "Vek nebol zadaný"}), 400
    if sex == None:
        return jsonify({"error": "Pohlavie nebolo zadané"}), 400
    if not breed:
        return jsonify({"error": "Plemeno nebolo zadané"}), 400
    else:
        try:
            models.Breed.get(models.Breed.id == breed)
        except peewee.DoesNotExist:
            return jsonify({"error": "Dané plemeno neexistuje"}), 400
        except:
            return Response('server_error')
    if not health_status:
        return jsonify({"error": "Zdravotný stav nebol zadaný"}), 400
    else:
        try:
            models.HealthStatus.get(models.HealthStatus.id == health_status)
        except peewee.DoesNotExist:
            return jsonify({"error": "Daný zdravotný stav neexistuje"}), 400
        except:
            return Response('server_error')
    if not castrated:
        castrated = False
    if not vaccinated:
        vaccinated = False
    if not dewormed:
        dewormed = False
    if not colour:
        return jsonify({"error": "Farba srsti nebola zadaná"}), 400
    else:
        try:
            models.Colour.get(models.Colour.id == colour)
        except peewee.DoesNotExist:
            return jsonify({"error": "Daná farba neexistuje"}), 400
        except:
            return Response('server_error')

    if not description:
        return jsonify({"error": "Popis nebol zadaný"}), 400
    if not adoptive:
        adoptive = False
    if not pictures:
        return jsonify({"error": "Nebol pridaný žiadny obrázok"}), 400

    if not isinstance(name, str) or not isinstance(age, int) or not isinstance(sex, bool) or not isinstance(castrated, bool) or not isinstance(vaccinated, bool) or not isinstance(dewormed, bool) or not isinstance(description, str) or not isinstance(health_log, str) or not isinstance(adoptive, bool) or not isinstance(pictures, list):
        return Response('invalid_format')

    if int(age) < 0 or int(age) > 300:
        return jsonify({"error": "Neplatná hodnota veku"}), 400

    for p in pictures:
        try:
            models.Picture.get(models.Picture.uuid == p)
        except peewee.DoesNotExist:
            return jsonify({"error": "Daný obrázok neexistuje"}), 400
        except:
            return Response('server_error')

    cat = models.Cat(uuid=uuid.uuid4(), name=Sanitize(name), age=age, sex=sex, breed=breed, health_status=health_status, castrated=castrated, vaccinated=vaccinated,
                     dewormed=dewormed, colour=colour, description=Sanitize(description, False), health_log=Sanitize(health_log, False), adoptive=adoptive, pictures=json.dumps(pictures))

    try:
        cat.save()
    except:
        return Response('server_error')

    return jsonify({'uuid': cat.uuid}), 200


@app.route('/cats/<uuid>', methods=['PUT'])
@jwt_required
def cats_update(uuid):
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
        match = models.Cat.get(models.Cat.uuid == uuid)
    except peewee.DoesNotExist:
        return Response('invalid')
    except:
        return Response('server_error')

    try:
        name = request.json.get('name', None)
        age = request.json.get('age', None)
        sex = request.json.get('sex', None)
        breed = request.json.get('breed', None)
        health_status = request.json.get('health_status', None)
        castrated = request.json.get('castrated', None)
        vaccinated = request.json.get('vaccinated', None)
        dewormed = request.json.get('dewormed', None)
        colour = request.json.get('colour', None)
        description = request.json.get('description', None)
        health_log = request.json.get('health_log', None)
        adoptive = request.json.get('adoptive', None)
        pictures = request.json.get('pictures', None)
    except:
        return Response('not_json')

    try:
        request.json['health_log']
        update_health_log = True
    except KeyError:
        update_health_log = False

    if (not name) and (not age) and (sex == None) and (not breed) and (not health_status) and (castrated == None) and (vaccinated == None) and (dewormed == None) and (not colour) and (not description) and (health_log == None and not update_health_log) and (adoptive == None) and (not pictures):
        return Response('empty')

    if name:
        if not isinstance(name, str):
            return Response('invalid_format')
        match.name = Sanitize(name)
    if age:
        if not isinstance(age, int) or int(age) < 0 or int(age) > 300:
            return jsonify({"error": "Neplatná hodnota veku"}), 400
        match.age = age
    if sex != None:
        if not isinstance(sex, bool):
            return Response('invalid_format')
        match.sex = sex
    if breed:
        if not isinstance(breed, int):
            return Response('invalid_format')
        try:
            models.Breed.get(models.Breed.id == breed)
            match.breed = breed
        except peewee.DoesNotExist:
            return jsonify({"error": "Dané plemeno neexistuje"}), 400
        except:
            return Response('server_error')
    if health_status:
        if not isinstance(health_status, int):
            return Response('invalid_format')
        try:
            models.HealthStatus.get(models.HealthStatus.id == health_status)
            match.health_status = health_status
        except peewee.DoesNotExist:
            return jsonify({"error": "Daný zdravotný stav neexistuje"}), 400
        except:
            return Response('server_error')
    if castrated != None:
        if not isinstance(castrated, bool):
            return Response('invalid_format')
        match.castrated = castrated
    if vaccinated != None:
        if not isinstance(vaccinated, bool):
            return Response('invalid_format')
        match.vaccinated = vaccinated
    if dewormed:
        if not isinstance(dewormed, bool):
            return Response('invalid_format')
        match.dewormed = dewormed
    if colour:
        if not isinstance(colour, int):
            return Response('invalid_format')
        try:
            models.Colour.get(models.Colour.id == colour)
            match.colour = colour
        except peewee.DoesNotExist:
            return jsonify({"error": "Daná farba neexistuje"}), 400
        except:
            return Response('server_error')

    if description:
        if not isinstance(description, str):
            return Response('invalid_format')
        match.description = Sanitize(description, False)

    if update_health_log:
        if not isinstance(health_log, str):
            return Response('invalid_format')
        match.health_log = Sanitize(health_log, False)

    if adoptive != None:
        if not isinstance(adoptive, bool):
            return Response('invalid_format')
        match.adoptive = adoptive
    if pictures:
        if not isinstance(pictures, list):
            return Response('invalid_format')
        for p in pictures:
            try:
                models.Picture.get(models.Picture.uuid == p)
            except peewee.DoesNotExist:
                return jsonify({"error": "Daný obrázok neexistuje"}), 400
            except:
                return Response('server_error')
        match.pictures = json.dumps(pictures)

    try:
        match.save()
    except:
        return jsonify({'error': 'Mačku nebolo možné uložiť'}), 400

    return Response('empty')


@app.route('/cats/<uuid>', methods=['DELETE'])
@jwt_required
def cats_delete(uuid):
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
        match = models.Cat.get(models.Cat.uuid == uuid)
    except peewee.DoesNotExist:
        return Response('invalid')
    except:
        return Response('server_error')

    match.delete_instance()

    return Response('empty')


@app.route('/cats/<uuid>/adopt', methods=['POST'])
@jwt_required
def cats_adopt(uuid):
    # get current user
    current_user = get_jwt_identity()
    try:
        # if user does not exist in DB, forbidden
        user = models.User.get(models.User.uuid == current_user)
    except:
        return Response('forbidden')

    try:
        match = models.Cat.get(models.Cat.uuid == uuid)
    except peewee.DoesNotExist:
        return Response('invalid')
    except:
        return Response('server_error')

    if not match.adoptive or (match.adopted_by and match.adopted_by != user.uuid):
        return jsonify({'error': 'Mačku nie je možné adoptovať'}), 400

    if match.adopted_by == user.uuid:
        match.adoptive = True
        match.adopted_by = None
    else:
        match.adoptive = False
        match.adopted_by = user.uuid

    try:
        match.save()
    except:
        return Response('server_error')

    return Response('empty')


@app.route('/cats/<uuid>/like', methods=['POST'])
@jwt_required
def cats_like(uuid):
    # get current user
    current_user = get_jwt_identity()
    try:
        # if user does not exist in DB, forbidden
        user = models.User.get(models.User.uuid == current_user)
    except:
        return Response('forbidden')

    try:
        models.Cat.get(models.Cat.uuid == uuid)
    except peewee.DoesNotExist:
        return Response('invalid')
    except:
        return Response('server_error')

    try:
        models.Favourite.get(models.Favourite.user ==
                             user.uuid and models.Favourite.cat == uuid)
    except peewee.DoesNotExist:
        favourite = models.Favourite(user=user.uuid, cat=uuid)
        favourite.save()
    except:
        return Response('server_error')

    return Response('empty')


@app.route('/cats/<uuid>/unlike', methods=['POST'])
@jwt_required
def cats_unlike(uuid):
    # get current user
    current_user = get_jwt_identity()
    try:
        # if user does not exist in DB, forbidden
        user = models.User.get(models.User.uuid == current_user)
    except:
        return Response('forbidden')

    try:
        models.Cat.get(models.Cat.uuid == uuid)
    except peewee.DoesNotExist:
        return Response('invalid')
    except:
        return Response('server_error')

    try:
        favourite = models.Favourite.get(
            models.Favourite.user == user.uuid and models.Favourite.cat == uuid)
        favourite.delete_instance()
    except peewee.DoesNotExist:
        return Response('empty')
    except:
        return Response('server_error')

    return Response('empty')
