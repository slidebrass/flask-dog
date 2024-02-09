from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, user_schema, users_schema, BreedNotes, breed_notes_schema, breeds_notes_schema, BreedInfo, breed_info_schema, breeds_info_schema

api = Blueprint('api',__name__, url_prefix='/api')

# Users Routes
@api.route('/users', methods = ['POST'])
@token_required
# to save user information and favorite breeds
def create_user(current_user_token):
    id = request.json['id']
    breedNotes_Id = request.json['breedNotes_Id']
    user_token = current_user_token.token

    user = User(id, breedNotes_Id, user_token = user_token)

    db.session.add(user)
    db.session.commit()

    response = user_schema.dump(user)
    return jsonify(response)

@api.route('/users', methods = ['GET'])
@token_required
def get_users(current_user_token):
    a_user = current_user_token.token
    users = User.query.filter_by(user_token = a_user).all()
    response = users_schema.dump(users)
    return jsonify(response)

@api.route('/users/<id>', methods = ['GET'])
@token_required
def get_user(current_user_token, id):
    a_user = current_user_token.token
    user = User.query.get(id)
    response = user_schema.dump(user)
    return jsonify(response)

@api.route('/users/<id>', methods = ['PUT'])
@token_required
def update_user(current_user_token, id):
    user = User.query.get(id)
    user.breedNotes_Id = request.json['breedNotes_Id']
    user.user_token = current_user_token.token

    db.session.commit()
    response = user_schema.dump(user)
    return jsonify(response)

@api.route('/users/<id>', methods = ['DELETE'])
@token_required
def delete_user(current_user_token, id):
    user = User.query.get(id)
    db.session.delte(user)
    db.session.commit()
    response = user_schema.dump(user)
    return jsonify(response)

# Notes Routes
@api.route('/notes', methods = ['POST'])
@token_required
# to create and save notes to a user's account
def create_note(current_user_token):
    breedNotes_Id = request.json['breedNotes_Id']
    notes = request.json['notes']
    breed_id = request.json['breed_id']
    user_token = current_user_token.token

    breed_notes = BreedNotes(breedNotes_Id, notes, breed_id, user_token = user_token)

    db.session.add(breed_notes)
    db.session.commit()

    response = breed_notes_schema.dump(breed_notes)
    return jsonify(response)

@api.route('/notes', methods = ['GET'])
@token_required
def get_notes(current_user_token):
    a_user = current_user_token.token
    breed_notes = BreedNotes.query.get(user_token = a_user).all()
    response = breeds_notes_schema.dump(breed_notes)
    return jsonify(response)

@api.route('/notes/<breedNotes_Id>', methods = ['GET'])
@token_required
def get_note(current_user_token, breedNotes_Id):
    breed_note = BreedNotes.query.get(breedNotes_Id)
    response = breed_notes_schema.dump(breed_note)
    return jsonify(response)

@api.route('/notes/<breedNotes_Id>', methods = ['PUT'])
@token_required
def update_notes(current_user_token, breed_notes_Id):
    breed_notes = BreedNotes.query.get(breedNotes_Id)
    breed_notes.notes = request.json['notes']
    breed_notes.breed_id = request.json['breed_id']
    breed_notes.user_token = current_user_token.token

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
@api.route('/dogs', methods = ['POST'])
@token_required
# information to come from 3rd party API call
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

@api.route('/dogs', methods = ['GET'])
@token_required
def get_dogs(current_token):
    dogs = BreedInfo.query.filter_by(current_token.token).all()
    response = breeds_info_schema.dump(dogs)
    return jsonify(response)

@api.route('/dogs/<breed_id>', methods = ['GET'])
@token_required
def get_dog(current_user_token, breed_id):
    dog = BreedInfo.query.get(breed_id)
    response = breed_info_schema.dump(dog)
    return jsonify(response)

@api.route('/dogs/<breed_id>', methods = ['DELETE'])
@token_required
def delete_dog(current_user_token, breed_id):
    dog = BreedInfo.query.get(breed_id)
    db.session.delete(dog)
    db.session.commit()
    response = breed_info_schema.dump(dog)
    return jsonify(response)