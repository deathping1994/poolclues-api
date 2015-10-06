from app import db,app
import datetime
from flask.ext.sqlalchemy import SQLAlchemy


db = SQLAlchemy(app)
event_id_sequence= db.Sequence('event_id_seq', start=101,increment=1)


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


class ContactNumber(db.Model):
    email_id= db.Column(db.String(80), db.ForeignKey(User.email_id), primary_key=True)
    contact_no= db.Column(db.String(20), primary_key=True, nullable=False)

    def __init__(self,email_id,contact_no):
        self.email_id = email_id
        self.contact_no=contact_no

    def __repr__(self):
        return '<ContactNumber %r %s>' % self.email_id, self.contact_no


# class Creator(db.Model):
#     email_id=db.Column(db.String(80),db.ForeignKey(User.email_id),primary_key=True)
#     event_id=db.Column(db.Integer,event_id_sequence,autoincrement=True,primary_key=True)
#
#     def __init__(self,email_id):
#         self.email_id=email_id
#
#     def __repr__(self):
#         return '<Creator %r %r>' % self.email_id,self.event_id


class Event(db.Model):
    email_id=db.Column(db.String(80),db.ForeignKey(User.email_id))
    event_id= db.Column(db.Integer,event_id_sequence,autoincrement=True,primary_key=True)
    event_name=db.Column(db.String(80),nullable=False)
    target_date=db.Column(db.Date,nullable=False)
    target_amount=db.Column(db.Float,nullable=False)
    description=db.Column(db.Text,nullable=False)
    date_created=db.Column(db.Date,nullable=False)

    def __init__(self,email_id,event_name,target_date,target_amount,description):
        self.email_id=email_id
        self.event_name=event_name
        self.target_date=target_date
        self.date_created=datetime.datetime.now().date()
        self.target_amount=target_amount
        self.description=description


__author__ = 'gaurav'

