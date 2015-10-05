import datetime
from flask import jsonify
from flask import Flask,request
from flask.ext.bcrypt import Bcrypt
from flask.ext.sqlalchemy import SQLAlchemy
import models
from flask.ext.pymongo import PyMongo
import sqlalchemy.exc
from flask.ext.cors import CORS,cross_origin


app = Flask("poolclues")
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:gaurav@localhost:5432/poolclues'
bcrypt=Bcrypt(app)
mongo = PyMongo(app)
db = SQLAlchemy(app)
cors = CORS(app, resources={r"*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

def start_session(email_id,authtoken):
    try:
        res=mongo.db.session.insert({"user":email_id,"authtoken":authtoken})
        return True
    except Exception:
        return False
def stop_session(email_id,authtoken):
    try:
        mongo.db.session.remove({"user":email_id,"authtoken":authtoken})
        return True
    except Exception:
        return False

def log(e):
    try:
        data={"exception":str(e),
            "time": datetime.datetime.now()}
        mongo.db.poolclueslog.insert(data)
    except Exception:
        return jsonify(error="This time something seriously went wrong event log server is down"),500


@app.route('/register',methods=["GET","POST"])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
def index():
    print "inside index"
    data=request.get_json(force=True)
    print(data)
    db.create_all()
    user = models.User(data['first_name'],data['middle_name'],data['last_name'], data['email_id'],
                 bcrypt.generate_password_hash(data['password']),data['house_no'],data['street'],
                 data['city'],data['state'],data['country'])
    # guest = User('guest', 'guest@example.com')
    try:
        db.session.add(user)
        # db.session.add(guest)
        db.session.commit()
        return jsonify(success="User successfully registered"),200
    except Exception as e:
        print type(e)
        if isinstance(e,sqlalchemy.exc.IntegrityError):
            return jsonify(error="User already Exists"),500
        else:
            log(e)
            return jsonify(error="Oops something went wrong. Contact administrator"),500


@app.route('/authenticate',methods=["POST"])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
def auth():
    data=request.get_json(force=True)
    try:
        if len(data['email_id'])!=0 and len(data['password'])!=0:
            print "inside if"
            user= models.User.query.get(data['email_id'])
            password= data['password'].encode()
            if user is not None:
                if bcrypt.check_password_hash(user._password.encode('utf-8'),password):
                    authtoken=bcrypt.generate_password_hash(user.email_id+str(datetime.datetime.now()))
                    if start_session(user.email_id,authtoken):
                        return jsonify(success="Successfully Logged in !",authtoken=authtoken)
                    else:
                        raise Exception
                else:
                    return jsonify(error="Incorrect username and password"),403
            else:
                return jsonify(error="User does not exist"),403
        else:
            return jsonify(error="Incomplete Details Provided"),500
    except Exception as e:
        if isinstance(e,KeyError):
            return jsonify(error="Key error, send all required fields"),400
        else:
            print e
            log(e)
            return jsonify(error="Something Went wrong the event has been recorded and will soon be fixed."),500


@app.route('/logout/<email_id>',methods=["GET","POST"])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
def logout(email_id):
    data=request.get_json(force=True)
    try:
        if "authtoken" in data:
            if stop_session(email_id,data['authtoken']):
                return jsonify(success="Successfully logged off"),200
            else:
                return jsonify(error="Could not log you off. Try again"),500
        else:
            return jsonify(error="Authtoken missing in payload."),500
    except Exception as e:
        log(e)
        return jsonify(error="Something went wrong. You might not be logged off so check it before leaving."),500


@app.route('/')
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
def test():
    return jsonify(success="It works")

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8080,debug=True)
