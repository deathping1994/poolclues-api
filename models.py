from flaskapp import db
import datetime
event_id_sequence="101"
__author__ = 'gaurav'

class User(db.Model):
    email_id= db.Column(db.String(80), unique=True,primary_key=True,nullable=False)
    _password= db.Column(db.String(20),nullable=False)
    first_name=db.Column(db.String(20),nullable=False)
    middle_name= db.Column(db.String(20),nullable=True)
    last_name = db.Column(db.String(20),nullable=True)
    house_number=db.Column(db.String(40),nullable=True)
    street=db.Column(db.String(40),nullable=True)
    city= db.Column(db.String(20),nullable=True)
    state=db.Column(db.String(20),nullable=True)
    country=db.Column(db.String(20),nullable=False)

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

    def __repr__(self):
        return '<User %r>' % self.username


class ContactNumber(db.Model):
    email_id= db.Column(db.String(80), db.ForeignKey(User.email_id), primary_key=True)
    contact_no= db.Column(db.String(20), primary_key=True, nullable=False)

    def __init__(self,email_id,contact_no):
        self.email_id = email_id
        self.contact_no=contact_no

    def __repr__(self):
        return '<ContactNumber %r %s>' % self.email_id, self.contact_no


class Event(db.Model):
    event_id= db.Column(db.Integer,db.Sequence(event_id_sequence),primary_key=True)
    event_name=db.Column(db.String(80),nullable=False)
    target_date=db.Column(db.DateTime,nullable=False)
    target_amount=db.Column(db.Float,nullable=False)
    description=db.Column(db.Text,nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.datetime.now)

    def __init__(self,event_name,date_created,target_date,target_amount,description):
        self.event_name=event_name
        self.date_created=date_created
        self.target_date=target_date
        self.target_amount=target_amount
        self.description=description


    def __repr__(self):
        return '<Event %r %s>' % self.event_id_id, self.event_name


class Creator(db.Model):
    email_id= db.Column(db.String(80),db.ForeignKey(User.email_id),primary_key=True)
    event_id= db.Column(db.Integer,db.Sequence(event_id_sequence),db.ForeignKey(Event.event_id),primary_key=True)

    def __init__(self,email_id):
        self.email_id = email_id

    def __repr__(self):
        return '<Creator %r %s>' % self.email_id, self.event_id
