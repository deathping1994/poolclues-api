import os
from datetime import datetime
from flask import jsonify
from flask import Flask, request, flash, url_for, redirect, \
     render_template, abort, send_from_directory
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import sqlalchemy.exc
app = Flask(__name__)
app.config.from_pyfile('flaskapp.cfg')

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/')
def index():
    admin = User('admin', 'admin@example.com')
    guest = User('guest', 'guest@example.com')
    try:
        db.session.add(admin)
        db.session.add(guest)
        db.session.commit()
        return jsonify(success="Records inserted"),200
    except sqlalchemy.exc.IntegrityError as e:
        return jsonify(error="Duplicate values"),500

@app.route('/register')
def test():
    data=request.get_json(force=True)
    if "Gaurav"==data['user']:
        return josnify(error="User already exits"),500
    else:
        return jsonify(success="user created"),200


@app.route('/event/create')
def fail():
    return jsonify(error="You can read the error"),500


@app.route('/<path:resource>')
def serveStaticResource(resource):
    return send_from_directory('static/', resource)


if __name__ == '__main__':
    app.run()
