from flask import jsonify
from flask import Flask,request
from flask.ext.bcrypt import Bcrypt
from flask.ext.sqlalchemy import SQLAlchemy
import sqlalchemy.exc

app = Flask("poolclues")
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:gaurav@localhost:5432/poolclues'
bcrypt=Bcrypt(app)
db = SQLAlchemy(app)


class User(db.Model):
    email_id= db.Column(db.String(80), unique=True,primary_key=True,nullable=False)
    _password= db.Column(db.String(100),nullable=False)
    first_name=db.Column(db.String(20),nullable=False)
    middle_name= db.Column(db.String(20),nullable=True)
    last_name = db.Column(db.String(20),nullable=True)
    house_number=db.Column(db.String(40),nullable=True)
    street=db.Column(db.String(40),nullable=True)
    city= db.Column(db.String(20),nullable=True)
    state=db.Column(db.String(20),nullable=True)
    country=db.Column(db.String(20),nullable=False)
    verified=db.Column(db.Boolean,default=False,nullable=False)

    def __init__(self, first_name,middle_name,last_name,email_id,_password,house_number,street,city,state,country):
        self.first_name = first_name
        self.middle_name=middle_name
        self.last_name=last_name
        self.email_id = email_id
        self._password=_password
        self.house_number=house_number
        self.street=street
        self.city=city
        self.state=state
        self.country=country
        self.verified=False


@app.route('/register',methods=["GET","POST"])
def index():
    print "inside index"
    data=request.get_json(force=True)
    print(data)
    db.create_all()
    user = User(data['first_name'],data['middle_name'],data['last_name'], data['email_id'],
                 bcrypt.generate_password_hash(data['password']),data['house_no'],data['street'],
                 data['city'],data['state'],data['country'])
    # guest = User('guest', 'guest@example.com')
    try:
        db.session.add(user)
        # db.session.add(guest)
        db.session.commit()
        return jsonify(success="User successfully registered"),200
    except Exception as e:
        print e
        return jsonify(error="Oops something went wrong. Contact administrator"),500


@app.route('/')
def test():
    return jsonify(success="It works")

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8080,debug=True)
