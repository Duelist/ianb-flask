from flask import Flask
from flask.ext.mongoengine import MongoEngine
from ianb import local_settings

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = local_settings.mongo_settings
app.config['SECRET_KEY'] = local_settings.secret_key
db = MongoEngine(app)

from ianb import models, views