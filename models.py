from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import uuid
import secrets

ma = Marshmallow()
db = SQLAlchemy()

# Establish class User to allow users to save favorite breeds to a table linked to their account
class User(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    breedNotes_Id = db.Column(db.String, db.ForeignKey('breednotes.breedNotes_Id'), nullable=False)
    token = db.Column(db.String, default='', unique=True)

    # Setting unique user_id
    def __init__(self, breedNotes_Id, token=''):
        self.id = self.set_id()
        self.breedNotes_Id = breedNotes_Id
        self.token = self.set_token(24)

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())
        
class UserSchema(ma.Schema):
    class Meta:
        fields = ['id', 'breedNotes_Id']

user_schema = UserSchema()
users_schema = User(UserSchema(many=True))

# creating a class to store breed information gathered from the Dog API
class BreedInfo(db.Model):
    __tablename__ = 'breedinfo'
    breed_id = db.Column(db.String(36), primary_key=True)
    breed_name = db.Column(db.String(100))
    breed_group = db.Column(db.String(100))
    life_span = db.Column(db.String(100))
    weight = db.Column(db.String(100))
    height = db.Column(db.String(100))
    bred_for = db.Column(db.String(200))
    temperament = db.Column(db.String(500))
    reference_image_id = db.Column(db.String(50))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable=False)

    def __init__(self, breed_id, breed_name, breed_group, life_span, weight, height, bred_for, temperament, reference_image_id, user_token):
        self.breed_id = self.set_id()
        self.breed_name = breed_name
        self.breed_group = breed_group
        self.life_span = life_span
        self.weight = weight
        self.height = height
        self.bred_for = bred_for
        self.temperament = temperament
        self.reference_image_id = reference_image_id
        self.user_token = user_token

    def set_id(self):
        return str(uuid.uuid4())
    
    def __repr__(self):
        return f'The {self.breed_name} breed has been added to your favorites.'
    
class BreedInfoSchema(ma.Schema):
    class Meta:
        fields = ['breed_id', 'breed_name', 'breed_group', 'life_span', 'weight', 'height', 'bred_for', 'temperament', 'reference_image_id']

breed_info_schema = BreedInfoSchema()
breeds_info_schema = BreedInfoSchema(many=True)

# Establish class to allow users to write notes about their favorite breeds that 
# will show up when they look at their favorites
class BreedNotes(db.Model):
    __tablename__ = 'breednotes'
    breedNotes_Id = db.Column(db.String(36), primary_key=True)
    notes = db.Column(db.String(500))
    breed_id = db.Column(db.String(36), db.ForeignKey('breedinfo.breed_id'), nullable=False)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable=False)

    # setting unique id for breedNotes
    def __init__(self, notes, breed_id, user_token, breedNotes_Id=''):
        self.breedNotes_Id = self.set_id()
        self.notes = notes
        self.breed_id = breed_id
        self.user_token = user_token

    def set_id(self):
        return str(uuid.uuid4())
        
class BreedNotesSchema(ma.Schema):
    class Meta:
        fields = ['breedNotes_Id', 'notes', 'breed_id']

breed_notes_schema = BreedNotesSchema()
breeds_notes_schema = BreedNotesSchema(many=True)