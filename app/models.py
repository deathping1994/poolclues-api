from app import app,db
import datetime
from flask.ext.sqlalchemy import SQLAlchemy
pool_id_sequence= db.Sequence('event_id_seq', start=101,increment=1)



class Pool(db.Model):
    pool_id=db.Column(db.Integer,pool_id_sequence,autoincrement=True,primary_key=True)
    public=db.Column(db.Boolean,default=True)
    def __init__(self,public=True):
        self.public=True



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


class Transaction(db.Model):
    transaction_id=db.Column(db.String(80),primary_key=True)
    email_id=db.Column(db.String(80),db.ForeignKey(User.email_id),primary_key=True)
    amount=db.Column(db.Float)
    date=db.Column(db.Date,nullable=False)
    pool_id=db.Column(db.String(10))

    def __init__(self,email_id,transaction_id,amount,pool_id=''):
        self.email_id=email_id
        self.transaction_id=transaction_id
        self.amount=amount
        self.pool_id=pool_id
        self.date=datetime.datetime.now().date()


class Event(db.Model):
    email_id=db.Column(db.String(80),db.ForeignKey(User.email_id))
    event_id= db.Column(db.Integer,db.ForeignKey(Pool.pool_id),primary_key=True)
    event_name=db.Column(db.String(80),nullable=False)
    target_date=db.Column(db.Date,nullable=False)
    target_amount=db.Column(db.Float,nullable=False)
    description=db.Column(db.Text,nullable=False)
    date_created=db.Column(db.Date,nullable=False)
    public=db.Column(db.Boolean,default=True)

    def __init__(self,event_id,email_id,event_name,target_date,target_amount,description,public=True):
        self.email_id=email_id
        self.event_id=event_id
        self.event_name=event_name
        self.target_date=target_date
        self.date_created=datetime.datetime.now().date()
        self.target_amount=target_amount
        self.description=description
        self.public=public



class GiftBucket(db.Model):
    event_id= db.Column(db.Integer,db.ForeignKey(Pool.pool_id),primary_key=True)
    product_id=db.Column(db.String(10),primary_key=True)

    def __init__(self,event_id,product_id):
        self.event_id=event_id
        self.product_id=product_id


class Invitee(db.Model):
    email_id=db.Column(db.String(80),nullable=False,primary_key=True)
    event_id=db.Column(db.Integer,db.ForeignKey(Pool.pool_id),primary_key=True)
    amount=db.Column(db.Float)
    transaction_id=db.Column(db.String(100),nullable=False)

    def __init__(self,email,event_id,amount,transaction_id=''):
        self.email_id=email
        self.event_id=event_id
        self.amount=amount
        print transaction_id
        self.transaction_id=transaction_id


class Registry(db.Model):
    email_id=db.Column(db.String(80),db.ForeignKey(User.email_id))
    registry_id= db.Column(db.Integer,db.ForeignKey(Pool.pool_id),primary_key=True)
    registry_name=db.Column(db.String(80),nullable=False)
    target_date=db.Column(db.Date,nullable=False)
    description=db.Column(db.Text,nullable=False)
    date_created=db.Column(db.Date,nullable=False)
    public=db.Column(db.Boolean,default=True)

    def __init__(self,registry_id,email_id,registry_name,target_date,description,public=True):
        self.email_id=email_id
        self.registry_id=registry_id
        self.registry_name=registry_name
        self.target_date=target_date
        self.date_created=datetime.datetime.now().date()
        self.description=description
        self.public=public


class Wallet(db.Model):
    email_id=db.Column(db.String(80),nullable=False,primary_key=True)
    amount=db.Column(db.Float)

    def __init__(self,email,amount):
        self.email_id=email
        self.amount=amount



__author__ = 'gaurav'

