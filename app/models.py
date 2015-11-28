from app import app,db
import datetime
from flask.ext.sqlalchemy import SQLAlchemy
event_id_sequence= db.Sequence('event_id_seq', start=101,increment=1)
post_id_sequence= db.Sequence('post_id_seq', start=10,increment=1)
comment_id_sequence= db.Sequence('comment_id_seq', start=20,increment=1)


class Event(db.Model):
    event_id=db.Column(db.Integer,event_id_sequence,autoincrement=True,primary_key=True)


class User(db.Model):
    email_id= db.Column(db.String(80), unique=True,primary_key=True,nullable=False)
    user_img= db.Column(db.String(80))
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

    def __init__(self, first_name,middle_name,last_name,email_id,_password,house_number,street,city,state,country,user_img="images/user.png"):
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
        self.user_img=user_img


class Registry(db.Model):
    email_id=db.Column(db.String(80),db.ForeignKey(User.email_id,ondelete='CASCADE'))
    registry_id= db.Column(db.Integer,db.ForeignKey(Event.event_id),primary_key=True)
    registry_name=db.Column(db.String(80),nullable=False)
    target_date=db.Column(db.Date,nullable=False)
    description=db.Column(db.Text,nullable=False)
    date_created=db.Column(db.Date,nullable=False)
    searchable=db.Column(db.Boolean,default=True)

    def __init__(self,registry_id,email_id,registry_name,target_date,description,searchable=True):
        self.email_id=email_id
        self.registry_id=registry_id
        self.registry_name=registry_name
        self.target_date=target_date
        self.date_created=datetime.datetime.now().date()
        self.description=description
        self.searchable=searchable


class Pool(db.Model):
    email_id=db.Column(db.String(80),db.ForeignKey(User.email_id,ondelete='CASCADE'))
    pool_id= db.Column(db.Integer,db.ForeignKey(Event.event_id),primary_key=True)
    pool_name=db.Column(db.String(80),nullable=False)
    pool_img=db.Column(db.String(100),default="images/pool.png")
    target_date=db.Column(db.Date,nullable=False)
    target_amount=db.Column(db.Float,nullable=False)
    description=db.Column(db.Text,nullable=False)
    date_created=db.Column(db.Date,nullable=False)
    searchable=db.Column(db.Boolean,default=True)

    def __init__(self,pool_id,email_id,pool_name,target_date,target_amount,description,searchable=True):
        self.email_id=email_id
        self.pool_id=pool_id
        self.pool_name=pool_name
        self.target_date=target_date
        self.date_created=datetime.datetime.now().date()
        self.target_amount=target_amount
        self.description=description
        self.searchable=searchable

    def upload_image(self,pool_img):
        self.pool_img=pool_img

    def modify_date(self,target_date):
        self.target_date=target_date

    def modify_target_amount(self,target_amount):
        self.target_amount=target_amount


class ContactNumber(db.Model):
    email_id= db.Column(db.String(80), db.ForeignKey(User.email_id), primary_key=True)
    contact_no= db.Column(db.String(20), primary_key=True, nullable=False)

    def __init__(self,email_id,contact_no):
        self.email_id = email_id
        self.contact_no=contact_no


class AlternateEmail(db.Model):
    email_id= db.Column(db.String(80), db.ForeignKey(User.email_id), primary_key=True)
    alt_email= db.Column(db.String(20), primary_key=True, nullable=False)

    def __init__(self,email_id,alt_email):
        self.email_id = email_id
        self.alt_email=alt_email


class ActivityFeed(db.Model):
    email_id=db.Column(db.String(80),db.ForeignKey(User.email_id),primary_key=True)
    display_str=db.Column(db.String(100))


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


class GiftBucket(db.Model):
    event_id= db.Column(db.Integer,db.ForeignKey(Event.event_id),primary_key=True)
    product_id=db.Column(db.String(10),primary_key=True)
    pool_id=db.Column(db.Integer,db.ForeignKey(Pool.pool_id,ondelete='CASCADE'))
    status=db.Column(db.String(10))

    def __init__(self,event_id,product_id):
        self.event_id=event_id
        self.product_id=product_id

    def start_pool(self,pool_id):
        self.pool_id=pool_id
        self.status="pooling"


class Invitee(db.Model):
    email_id=db.Column(db.String(80),nullable=False,primary_key=True)
    registry_id=db.Column(db.Integer,db.ForeignKey(Event.event_id,ondelete='CASCADE'),primary_key=True)

    def __init__(self,email,registry_id):
        self.email_id=email
        self.registry_id=registry_id


class Contributor(db.Model):
    email_id=db.Column(db.String(80),nullable=False,primary_key=True)
    pool_id=db.Column(db.Integer,db.ForeignKey(Pool.pool_id,ondelete='CASCADE'),primary_key=True)
    amount=db.Column(db.Float)
    amount_paid=db.Column(db.Float)
    status=db.Column(db.String(10),nullable=False)

    def __init__(self,email,pool_id,amount,status="UNPAID"):
        self.email_id=email
        self.pool_id=pool_id
        self.amount=amount
        self.status=status

    def make_payment(self,amount):
        self.amount_paid=self.amount-amount
        if self.amount_paid == self.amount:
            self.status="FUll"
        else:
            self.status="PART"

    def reject(self):
        self.status="Rejected"


class Post(db.Model):
    post_id=db.Column(db.Integer,post_id_sequence,autoincrement=True,primary_key=True)
    event_id=db.Column(db.Integer,db.ForeignKey(Event.event_id,ondelete='CASCADE'))
    content=db.Column(db.String(300))
    author=db.Column(db.String(80))

    def __init__(self,event_id,content,author):
        self.event_id=event_id
        self.content=content
        self.author=author


class Comment(db.Model):
    post_id=db.Column(db.Integer,db.ForeignKey(Post.post_id,ondelete='CASCADE'))
    comment_id=db.Column(db.Integer,comment_id_sequence,autoincrement=True,primary_key=True)
    content=db.Column(db.String(200))
    author=db.Column(db.String(80))

    def __init__(self,post_id,content,author):
        self.post_id=post_id
        self.content=content
        self.author=author


class Wallet(db.Model):
    email_id=db.Column(db.String(80),nullable=False,primary_key=True)
    amount=db.Column(db.Float)

    def __init__(self,email,amount):
        self.email_id=email
        self.amount=amount



__author__ = 'gaurav'

