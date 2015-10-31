from flask import Flask
from flask.ext.bcrypt import Bcrypt
# from routes import *
from flask.ext.pymongo import PyMongo
from flask.ext.cors import CORS
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask("poolclues")
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:gaurav@localhost:5432/poolclues'
bcrypt=Bcrypt(app)
mongo = PyMongo(app)
db=SQLAlchemy(app)
cors = CORS(app, resources={r"*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

__author__ = 'gaurav'
