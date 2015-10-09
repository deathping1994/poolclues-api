from app import bcrypt, app
from flask.ext.cors import cross_origin
from flask import request,jsonify
from models import *
from utilities import *
import sqlalchemy.exc
import requests


def sendmail(to,fromemail,message):
    try:
        data={'to':to,'fromemail':fromemail,'message':message}
        print requests.post("http://188.166.249.229/mailer.php",data=data).content
        return True
    except Exception as e:
        print "inside exception"
        print e
        log(e)
        return False


def sendinvite(to,fromemail,eventname,msg):
    message="Hi, "+fromemail+" has invited you to pool for "+eventname+ " on poolclues." +"\n"+msg
    print message
    if not sendmail(to,fromemail,message):
        return False
    else:
        return True

@app.route("/<email_id>/addphone/<phone>",methods=["POST"])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
def addphone(email_id,phone):
    try:
        contact=ContactNumber(email_id,phone)
        db.session.add(contact)
        db.session.commit()
        return jsonify(success="Contact added Successfully!"),201
    except Exception as e:
        log(e)
        return jsonify(error="Something went wrong.Could not add Phone number."),500


@app.route('/register',methods=["GET","POST"])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
def index():
    # import pdb; pdb.set_trace();
    print "inside index"
    data=request.get_json(force=True)
    print(data)
    db.create_all()
    user =User(data['first_name'],data['middle_name'],data['last_name'], data['email_id'],
               bcrypt.generate_password_hash(data['password']),data['house_no'],data['street'],
               data['city'],data['state'],data['country'])
    try:
        db.session.add(user)
        # db.session.add(guest)
        db.session.commit()
        if "phone" in data:
            addphone(data['email_id'],data['phone'])
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
            user= User.query.get(data['email_id'])
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


@app.route('/event/<event_id>',methods=["POST","GET"])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
def display_event(event_id):
    try:
        event= Event.query.get(event_id)
        return jsonify(event_id=event.event_id,event_name=event.event_name,target_date=str(event.target_date),
                       target_amount=event.target_amount,event_description=event.description),200
    except Exception as e:
        if isinstance(e,sqlalchemy.exc.SQLAlchemyError):
            return jsonify(error="Event Does not exist or some other sqlalchemy error"),500
        else:
            log(e)
            print e
            return jsonify(error="Something went wrong!"),500


@app.route('/<email_id>/event/list',methods=["POST","GET"])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
def user_event(email_id):
    try:
        events= Event.query.filter_by(email_id=email_id).all()
        eventlist=[]
        res={}
        if events is not None:
            for event in events:
                print event.event_id
                res['event_id']=event.event_id
                res['event_name']=event.event_name
                res['target_date']=str(event.target_date)
                res['date_created']=str(event.date_created)
                res['target_amount']=event.target_amount
                res['event_description']=event.description
                res['public']=event.public
                eventlist.append(res.copy())
                print eventlist
            return jsonify(event_list=eventlist),200
        else:
            return jsonify(error="No events found"),500
    except Exception as e:
        if isinstance(e,sqlalchemy.exc.SQLAlchemyError):
            return jsonify(error="Event Does not exist or some other sqlalchemy error"),500
        else:
            log(e)
            print e
            return jsonify(error="Something went wrong!"),500


@app.route('/event/create',methods=["POST","GET"])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
def create_event():
    try:
        # import pdb
        # pdb.set_trace()
        db.create_all()
        data=request.get_json(force=True)
        if len(data['event_name'])!=0:
            target_date=datetime.datetime.strptime(data['target_date'], "%d%m%Y").date()
            event=Event(data['email_id'],data['event_name'],target_date
                        ,data['target_amount'],data['description'])
            db.session.add(event)
            db.session.commit()
            event_id=event.event_id
            inviteSent=True
            failedlist=[]
            if "invites" in data:
                print "found invites"
                for invite in data['invites']:
                    print invite['email_id']
                    inviteentry=Invitee(invite['email_id'],event.event_id)
                    if not sendinvite(invite['email_id'],event.email_id,event.event_name,data['msg']):
                        inviteSent=False
                        failedlist.append(invite['email_id'])
                        print "inside  invite"
                        print inviteentry.email_id
                    else:
                        db.session.add(inviteentry)
                        db.session.commit()
            return jsonify(success="Event created successfully.",event_id=event_id,
                           failedlist=failedlist,inviteSent=inviteSent),201
        else:
            return jsonify(error="Event name field empty"),500
    except Exception as e:
        if isinstance(e,sqlalchemy.exc.IntegrityError):
            db.session.rollback()
            print e
            return jsonify(error="Event already Exists or User does not exists"),500
        else:
            print e
            log(e)
            return jsonify(error="Something went wrong!"),500


@app.route('/')
# @cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
def test():
    return jsonify(success="It works")




__author__ = 'gaurav'













