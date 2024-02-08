from flask import Flask, render_template
from config import Config
from .api.routes import api

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db as root_db, ma
from helpers import JSONEncoder

app = Flask(__name__)

app.json_encoder = JSONEncoder
app.config.from_object(Config)
root_db.init_app(app)
ma.init_app(app)
migrate = Migrate(app, root_db)