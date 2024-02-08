from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, user_schema, BreedNotes, breed_notes_schema, BreedInfo, breed_info_schema, breeds_info_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/dogs', methods = ['POST'])
@token_required
def create_breed_info(current_token):
    breed_id = request.json['breed_id']
    breed_name = request.json['breed_name']
    breed_group = request.json['breed_group']
    life_span = request.json['life_span']
    weight = request.json['weight']
    height = request.json['height']
    bred_for = request.json['bred_for']
    temperament = request.json['temperament']
    reference_iamge_id = request.json['reference_image_id']
    token = current_token.token

    # print(f'BIG TESTER: {current_token.token}')

    dog = BreedInfo(breed_id, breed_name, breed_group, life_span, weight, height, bred_for, temperament, reference_iamge_id, token = token)

    db.session.add(dog)
    db.session.commit()

    response = breed_info_schema.dump(dog)
    return jsonify(response)

# Do I need this? Can't really call multiple breeds currently. Should I search by breed_group instead?
@api.route('/dogs', methods = ['GET'])
@token_required
def get_dog(current_token):
    dogs = BreedInfo.query.filter_by(current_token.token).all()
    response = breed_info_schema.dump(dogs)
    return jsonify(response)

@api.route('/dogs/<breed_id>', methods = ['GET'])
@token_required
def get_single_dog(current_token, breed_id):
    dog = BreedInfo.query.get(breed_id)
    response = breed_info_schema.dump(dog)
    return jsonify(response)

# actually want to be able to just update the notes on the breed
@api.route('/dogs/<breed_id>', methods = ['PUT'])
@token_required
def update_dog(current_token, breed_id):
    dog = BreedInfo.query.get(breed_id)
    dog.breed_name = request.json['name']
    dog.breed_group = request.json['breed_group']

    db.session.commit()
    response = breed_info_schema.dump(dog)
    return jsonify(response)

# This is to delete dog from database. Need delete notes from database as well.
@api.route('/dogs/<breed_id>', methods = ['DELETE'])
@token_required
def delete_dog(current_token, breed_id):
    dog = BreedInfo.query.get(breed_id)
    db.session.delete(dog)
    db.session.commit()
    response = breed_info_schema.dump(dog)
    return jsonify(response)