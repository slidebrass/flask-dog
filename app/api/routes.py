from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, user_schema, users_schema, BreedNotes, breed_notes_schema
from models import breeds_notes_schema, BreedInfo, breed_info_schema, breeds_info_schema
from models import DogApiDict, dict_schema, dicts_schema
from models import Auth0Profile, profile_schema, profiles_schema
from sqlalchemy.sql import text

api = Blueprint('api',__name__, url_prefix='/api')

# Users Routes
@api.route('/users', methods = ['POST'])
@token_required
# to save user information and favorite breeds
def create_user(current_user_token):
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    user = User(first_name, last_name, email, token = token)

    db.session.add(user)
    db.session.commit()

    response = user_schema.dump(user)
    return jsonify(response)

@api.route('/users', methods = ['GET'])
@token_required
def get_users(current_user_token):
    users = User.query.filter_by(token = current_user_token.token).all()
    response = users_schema.dump(users)
    return jsonify(response)

@api.route('/users/<id>', methods = ['GET'])
@token_required
def get_user(current_user_token, id):
    # a_user = current_user_token.token
    user = User.query.get(id)
    response = user_schema.dump(user)
    return jsonify(response)

@api.route('/users/<id>', methods = ['PUT'])
@token_required
def update_user(current_user_token, id):
    user = User.query.get(id)
    token = current_user_token.token

    db.session.commit()
    response = user_schema.dump(user)
    return jsonify(response)

@api.route('/users/<id>', methods = ['DELETE'])
@token_required
def delete_user(token, id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    response = user_schema.dump(user)
    return jsonify(response)

# Auth0Profile Routes
@api.route('/profiles', methods = ['POST'])
@token_required
# creating a profile for the user
def create_profile(current_user_token):
    auth_user = request.json['auth_user']
    email = request.json['email']

    profile = Auth0Profile(auth_user, email)

    db.session.add(profile)
    db.session.commit()

    response = profile_schema.dump(profile)
    return jsonify(response)

# @api.route('/profiles', methods = ['GET'])
# @token_required
# retrieving profile information about the user
# def get_profile(current_user_token, ):


# Notes Routes
@api.route('/notes', methods = ['POST'])
@token_required
# to create and save notes to a user's account
def create_note(current_user_token):
    notes = request.json['notes']
    image_id = request.json['image_id']
    # user_token = current_user_token.token

    breed_notes = BreedNotes(notes, image_id)

    db.session.add(breed_notes)
    db.session.commit()

    response = breed_notes_schema.dump(breed_notes)
    return jsonify(response)

@api.route('/notes', methods = ['GET'])
@token_required
def get_notes(current_user_token):
    breed_notes = BreedNotes.query.filter_by(user_token = current_user_token.token).all()
    response = breeds_notes_schema.dump(breed_notes)
    return jsonify(response)

@api.route('/notes/<breedNotes_Id>', methods = ['GET'])
@token_required
def get_note(breedNotes_Id):
    breed_note = BreedNotes.query.get(breedNotes_Id)
    response = breed_notes_schema.dump(breed_note)
    return jsonify(response)

@api.route('/notes/<breedNotes_Id>', methods = ['PUT'])
@token_required
def update_notes(breedNotes_Id):
    breed_notes = BreedNotes.query.get(breedNotes_Id)
    breed_notes.notes = request.json['notes']
    breed_notes.image_id = request.json['image_id']
    breed_notes.id = request.json['id']
    
    # breed_notes.user_token = current_user_token.token

    db.session.commit()
    response = breed_notes_schema.dump(breed_notes)
    return jsonify(response)

@api.route('/notes/<breedNotes_Id>', methods = ['DELETE'])
@token_required
def delete_notes(current_user_token, breedNotes_Id):
    breed_notes = BreedNotes.query.get(breedNotes_Id)
    db.session.delete(breed_notes)
    db.session.commit()
    response = breed_notes_schema.dump(breed_notes)
    return jsonify(response)

# Breed Info Routes
@api.route('/info', methods = ['POST'])
@token_required
# information to come from 3rd party API call
def create_breed_info(current_user_token):
    breed_id = request.json['breed_id']
    breed_name = request.json['breed_name']
    breed_group = request.json['breed_group']
    life_span = request.json['life_span']
    weight = request.json['weight']
    height = request.json['height']
    bred_for = request.json['bred_for']
    temperament = request.json['temperament']
    reference_image_id = request.json['reference_image_id']
    user_token = current_user_token.token

    # print(f'BIG TESTER: {current_user_token.token}')

    dog = BreedInfo(breed_id, breed_name, breed_group, life_span, weight, height, bred_for, temperament, reference_image_id, user_token = user_token)

    db.session.add(dog)
    db.session.commit()

    response = breed_info_schema.dump(dog)
    return jsonify(response)

@api.route('/info', methods = ['GET'])
@token_required
def get_breeds_info(current_user_token):
    dogs = BreedInfo.query.filter_by(user_token = current_user_token.token).all()
    response = breeds_info_schema.dump(dogs)
    return jsonify(response)

@api.route('/info/<breed_info_id>', methods = ['GET'])
@token_required
def get_breed_info(current_user_token, breed_info_id):
    dog = BreedInfo.query.get(breed_info_id)
    response = breed_info_schema.dump(dog)
    return jsonify(response)

@api.route('/info/<breed_info_id>', methods = ['DELETE'])
@token_required
def delete_breed_info(current_user_token, breed_info_id):
    dog = BreedInfo.query.get(breed_info_id)
    db.session.delete(dog)
    db.session.commit()
    response = breed_info_schema.dump(dog)
    return jsonify(response)

# Dog Api Dict routes
@api.route('/dogdict', methods = ['POST'])
@token_required
def create_dogdict(current_token):
    dict_id = request.json['dict_id']
    dict_breed_name = request.json['dict_breed_name']
    dict_breed_id = request.json['dict_breed_id']
    token = current_token.token

    dog_dict = DogApiDict(dict_id, dict_breed_name, dict_breed_id, token)

    db.session.add(dog_dict)
    db.session.commit()

    response = dict_schema.dump(dog_dict)
    return jsonify(response)

@api.route('/dogdict', methods = ['GET'])
def get_dogdicts():
    dog_dict = DogApiDict.query.filter_by().all()
    response = dicts_schema.dump(dog_dict)
    return jsonify(response)

@api.route('/dogdict/<breed_name>', methods = ['GET'])
@token_required
def get_dogdict(current_user_token, breed_name):
    print('Calling GET')
    query = DogApiDict.query.filter(DogApiDict.dict_breed_name==breed_name).first()
    result = dict_schema.dump(query)
    print(result["dict_breed_id"])
    return jsonify(result["dict_breed_id"])

@api.route('/dogdict/<breed_name>', methods = ['GET'])
@token_required
def get_dogdict_image_id(current_user_token, breed_name):
    print('Calling GET image_id')
    query = DogApiDict.query.filter(DogApiDict.dict_breed_name==breed_name).first()
    result = dict_schema.dump(query)
    print(result["image_id"])
    return jsonify(result["image_id"])

@api.route('/dogdict/<dict_id>', methods = ['PUT'])
@token_required
def update_dog_dict(current_user_token, dict_id):
    print('Calling PUT')
    dog_dict = DogApiDict.query.get(dict_id)
    dog_dict.dict_breed_name = request.json['dict_breed_name']
    dog_dict.dict_breed_id = request.json['dict_breed_id']

    db.session.commit()
    response = dict_schema.dump(dog_dict)
    return jsonify(response)

@api.route('/dogdict/<dict_id>', methods = ['DELETE'])
@token_required
def delete_dogdict(current_user_token, dict_id):
    dog_dict = DogApiDict.query.get(dict_id)
    db.session.delete(dog_dict)
    db.session.commit()
    response = dict_schema.dump(dog_dict)
    return jsonify(response)