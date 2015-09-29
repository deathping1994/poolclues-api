import os
from datetime import datetime
from flask import jsonify
from flask import Flask, request, flash, url_for, redirect, \
     render_template, abort, send_from_directory

app = Flask(__name__)
app.config.from_pyfile('flaskapp.cfg')

@app.route('/')
def index():
    return render_template('index.html')

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
