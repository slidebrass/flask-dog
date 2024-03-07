from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager
from flask_marshmallow import Marshmallow
import secrets

login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Establish class User to allow users to save favorite breeds to a table linked to their account
class User(db.Model, UserMixin):
    id = db.Column(db.String(150), primary_key=True)
    first_name = db.Column(db.String(150), nullable=True, default = '')
    last_name = db.Column(db.String(150), nullable=True, default = '')
    email = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String, nullable=True, default='')
    g_auth_verify = db.Column(db.Boolean, default=False)
    token = db.Column(db.String, default='', unique=True)

    # Setting unique user_id
    def __init__(self, first_name, last_name, email, id='', password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash
    
    def __repr__(self):
        return f'User {self.email} has been added to the database.'
        
class UserSchema(ma.Schema):
    class Meta:
        fields = ['id', 'email', 'first_name', 'last_name', 'password']

user_schema = UserSchema()
users_schema = UserSchema(many=True)

# creating a class to store breed information gathered from the Dog API
class BreedInfo(db.Model):
    __tablename__ = 'breedinfo'
    breed_info_id = db.Column(db.String(150), primary_key=True)
    breed_id = db.Column(db.String)
    breed_name = db.Column(db.String(100))
    breed_group = db.Column(db.String(100))
    life_span = db.Column(db.String(100))
    weight = db.Column(db.String(100))
    height = db.Column(db.String(100))
    bred_for = db.Column(db.String(200))
    temperament = db.Column(db.String(500))
    reference_image_id = db.Column(db.String(50))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable=False)

    def __init__(self, breed_id, breed_name, breed_group, life_span, weight, height, bred_for, temperament, reference_image_id, user_token, breed_info_id = ''):
        self.breed_info_id = self.set_id()
        self.breed_id = breed_id
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
        fields = ['breed_info_id', 'breed_id', 'breed_name', 'breed_group', 'life_span', 'weight', 'height', 'bred_for', 'temperament', 'reference_image_id']

breed_info_schema = BreedInfoSchema()
breeds_info_schema = BreedInfoSchema(many=True)

# Establish class to allow users to write notes about their favorite breeds that 
# will show up when they look at their favorites
class BreedNotes(db.Model):
    __tablename__ = 'breednotes'
    breedNotes_Id = db.Column(db.String, primary_key=True)
    notes = db.Column(db.String(500))
    id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    breed_info_id = db.Column(db.String, db.ForeignKey('breedinfo.breed_info_id'), nullable=False)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable=False)

    # setting unique id for breedNotes
    def __init__(self, notes, id, breed_info_id, current_token, breedNotes_Id=''):
        self.breedNotes_Id = self.set_id()
        self.notes = notes
        self.id = id
        self.breed_info_id = breed_info_id
        self.user_token = current_token

    def set_id(self):
        return str(uuid.uuid4())
        
class BreedNotesSchema(ma.Schema):
    class Meta:
        fields = ['breedNotes_Id', 'notes', 'id', 'breed_info_id']

breed_notes_schema = BreedNotesSchema()
breeds_notes_schema = BreedNotesSchema(many=True)

# Establish a class that stores breed_names and the breed_id provided by TheDogApi.
class DogApiDict(db.Model):
    __tablename__ = 'dogapidict'
    dict_id = db.Column(db.Integer, primary_key=True)
    dict_breed_name = db.Column(db.String)
    dict_breed_id = db.Column(db.Integer)

class DictSchema(ma.SQLAlchemySchema):
    class Meta:
        model = DogApiDict
        
    dict_id = ma.auto_field()
    dict_breed_name = ma.auto_field()
    dict_breed_id = ma.auto_field()

dict_schema = DictSchema()
dicts_schema = DictSchema(many=True)