from app import bcrypt, app
from flask.ext.cors import cross_origin
from flask import request
from models import *
from utilities import *
from sqlalchemy import and_
import sqlalchemy.exc


@app.route('/register',methods=["GET","POST"])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
def index():
    # import pdb; pdb.set_trace();
    # print "inside index"
    data=request.get_json(force=True)
    db.create_all()
    print(data)
    user =User(data['first_name'],data['middle_name'],data['last_name'], data['email_id'],
               bcrypt.generate_password_hash(data['password']),data['house_no'],data['street'],
               data['city'],data['state'],data['country'])
    try:
        db.session.add(user)
        # db.session.add(guest)
        db.session.flush()
        wallet=Wallet(user.email_id,0)
        db.session.add(wallet)
        db.session.commit()
        if "phone" in data:
            addphone(data['email_id'],data['phone'])
        send_verification_email(user.email_id)
        return jsonify(success="User successfully registered"),200
    except Exception as e:
        print type(e)
        if isinstance(e,sqlalchemy.exc.IntegrityError):
            return jsonify(error="User already Exists"),500
        else:
            log(e)
            print e
            return jsonify(error="Oops something went wrong. Contact administrator"),500


@app.route("/<user>/verify",methods=["POST"])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
@login_required
def verify_account(user):
    try:
        data=request.get_json(force=True)
        user=str(user)
        if current_user(data['authtoken'])==user:
            res=mongo.db.verification_code.find_one({"user":user})
            if res['verification_code']==data['verification_code']:
                record=User.query.get(user)
                record.verified=True
                db.session.commit()
                return jsonify(success="Email Successfully verified"),200
            else:
                return jsonify(error="Either you entered wrong verification code or your verification code has expired"),500
        else:
            return jsonify(error="user does not exist"),500
    except Exception as e:
        print e
        log(e)
        return jsonify(error="Something went wrong"),500


@app.route('/products/list',methods=["GET","POST"])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
def list_products():
    try:
        product={}
        products=[]
        for i in range(1,30):
            product['id']=i
            product['name']="dummy"+str(i)
            product['image']="http://cdn.shopclues.net/images/thumbnails/25029/320/320/201510081245551444388995.jpg"
            product['price']=100
            products.append(product.copy())
        return jsonify(products=products),200
    except Exception as e:
        print e
        log(e)
        return jsonify(error="Shopclues is down."),500


@app.route('/forgotpassword/<user>',methods=["POST","GET"])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
def forgot_password(user):
    try:
        print(user,type(user))
        userlist=User.query.get(str(user))
        if userlist is not None:
            rid= bcrypt.generate_password_hash(user + str(datetime.datetime.now())+"Forgot secret password")
            if password_change_request(user,rid):
                return jsonify(success="Password change request has been recorded check your email for further instructions."),200
            else:
                return jsonify(error="Cannot take password change request, Try again"),500
        else:
            return jsonify(error="User does not exist"),404
    except Exception as e:
        print e
        log(e)
        return jsonify(error="Something went wrong!"),500


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


@app.route("/<email_id>/addphone/<phone>",methods=["POST"])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
@login_required
def addphone(email_id,phone):
    try:
        data=request.get_json(force=True)
        if current_user(data['authtoken'])==email_id:
            contact=ContactNumber(email_id,phone)
            db.session.add(contact)
            db.session.commit()
            return jsonify(success="Contact added Successfully!"),201
        else:
            return jsonify(error="You are not authorised to modify this account"),403
    except Exception as e:
        log(e)
        return jsonify(error="Something went wrong.Could not add Phone number."),500


@app.route('/<email_id>/event/list/<type>',methods=["POST","GET"])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
@login_required
def user_event(email_id,type):
    try:
        data=request.get_json(force=True)
        email_id=str(email_id)
        type=str(type)
        if current_user(data['authtoken'])==email_id:
            if type=="invited":
                sql="SELECT * FROM event where event_id IN (SELECT event_id from invitee where email_id ='"+email_id+"' )"
            elif type=="created":
                sql="SELECT * FROM event where email_id ='"+email_id+"'"
            elif type=="all":
                sql="SELECT * FROM event where event_id IN (SELECT event_id from invitee where email_id ='"+email_id+"' ) or email_id= '"+email_id+"'"
            events= db.engine.execute(sql)
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
        else:
            return jsonify(error="You are not authorised to view this event list."),403
    except Exception as e:
        if isinstance(e,sqlalchemy.exc.SQLAlchemyError):
            print e
            return jsonify(error="Event Does not exist or some other sqlalchemy error"),500
        else:
            log(e)
            print e
            return jsonify(error="Something went wrong!"),500


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

@app.route('/event/create',methods=["POST","GET"])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
@login_required
def create_event():
    try:
        db.create_all()
        data=request.get_json(force=True)
        if current_user(data['authtoken'])!=data['email_id']:
            return jsonify(error="You are not authorised to create events for this user"),403
        else:
            # import pdb
            # pdb.set_trace()
            db.create_all()
            if len(data['event_name'])!=0:
                target_date=datetime.datetime.strptime(data['target_date'], "%d%m%Y").date()
                pool=Pool()
                db.session.add(pool)
                db.session.flush()
                event=Event(pool.pool_id,data['email_id'],data['event_name'],target_date,data['target_amount'],data['description'])
                db.session.add(event)
                db.session.flush()
                event_id=event.event_id
                if "products" in data:
                    for pid in data['products']:
                        print event.event_id
                        giftbucket=GiftBucket(event.event_id,pid)
                        db.session.add(giftbucket)
                else:
                    voucher_code=get_voucher_code(data['target_amount'])
                    giftbucket=GiftBucket(event.event_id,voucher_code)
                    db.session.add(giftbucket)
                inviteSent=True
                failedlist=[]
                if "invites" in data:
                    num = len(data['invites'])
                    for invite in data['invites']:
                        if "amount" in invite:
                            inviteentry=Invitee(invite['email_id'],event.event_id,invite['amount'])
                        else:
                            amount=float(event.target_amount)/num
                            inviteentry=Invitee(invite['email_id'],event.event_id,amount)
                        if not sendinvite(invite['email_id'],event.email_id,event.event_name,data['msg']):
                            inviteSent=False
                            failedlist.append(invite['email_id'])
                        else:
                            db.session.add(inviteentry)
                            db.session.commit()
                else:
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
            db.session.rollback()
            return jsonify(error="Something went wrong!"),500


@app.route("/<user>/change/password/2",methods=["POST"])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
@login_required
def update_password2(user):
    try:
        user=str(user)
        data=request.get_json(force=True)
        if current_user(data['authtoken'])==user:
            record=User.query.get(user)
            print record._password
            record._password= bcrypt.generate_password_hash(data['new_password'])
            print record._password
            db.session.commit()
            return jsonify(success="Password Changed Successfully!"),200
        else:
            return jsonify(error="You are not authorised for this action"),500
    except Exception as e:
        print str(e)
        log(e)
        return jsonify(error="Something went wrong"),500



@app.route("/<user>/change/password",methods=["POST"])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
def update_password(user):
    try:
        user=str(user)
        data=request.get_json(force=True)
        res=mongo.db.password_change_requests.find_one({"user":user})
        if res is not None:
            if res['request_code']==data['request_code']:
                record=User.query.get(user)
                record._password= bcrypt.generate_password_hash(data['new_password'])
                db.session.commit()
                return jsonify(success="Password Changed Successfully!"),200
            else:
                return jsonify(error="You entered wrong request code!"),500
        else:
            e = user+" did not register a password change request! This event will be reported."
            log(e)
            return jsonify(error="User did not register a password change request! This event will be reported."),500
    except Exception as e:
        print e
        log(e)
        return jsonify(error="Something went wrong"),500


@app.route('/event/<eventid>/invite',methods=["POST","GET"])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
@login_required
def invite(eventid):
    try:
        data=request.get_json(force=True)
        event= Event.query.get(eventid)
        if current_user(data['authtoken'])!=event.email_id:
            return jsonify(error="You are not authorised to send invites for this event."),403
        else:
            inviteSent=True
            failedlist=[]
            for invite in data['invites']:
                if "amount" in invite:
                    inviteentry=Invitee(invite['email_id'],event.event_id,invite['amount'])
                else:
                    amount=event.target_amount/num
                    inviteentry=Invitee(invite['email_id'],event.event_id,amount)
                if not sendinvite(invite['email_id'],event.email_id,event.event_name,data['msg']):
                    inviteSent=False
                    failedlist.append(invite['email_id'])
                else:
                    db.session.add(inviteentry)
                    db.session.flush()
            if not inviteSent:
                return jsonify(error="Could not send out some invitations",failedlist=failedlist),500
            else:
                db.session.commit()
                return jsonify(success="All invitations sent successfully"),201
    except Exception as e:
        db.session.rollback()
        if isinstance(e,sqlalchemy.exc.IntegrityError):
            print e
            return jsonify(error="Something went wrong probably event does not exist or you the user has already been invited"),500
        else:
            print e
            log(e)
            return jsonify(error="Oops! something broke, we'll fix it soon."),500


@app.route('/registry/<registry_id>/invite',methods=["POST","GET"])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
@login_required
def registry_invite(registry_id):
    try:
        registry_id=str(registry_id)
        data=request.get_json(force=True)
        registry= Registry.query.get(registry_id)
        if current_user(data['authtoken'])!=registry.email_id:
            return jsonify(error="You are not authorised to send invites for this Registry."),403
        else:
            inviteSent=True
            failedlist=[]
            for invite in data['invites']:
                inviteentry=Invitee(invite['email_id'],registry.registry_id,0)
                if not sendinvite(invite['email_id'],registry.email_id,registry.registry_name,data['msg']):
                    inviteSent=False
                    failedlist.append(invite['email_id'])
                else:
                    db.session.add(inviteentry)
                    db.session.flush()
            if not inviteSent:
                return jsonify(error="Could not send out some invitations",failedlist=failedlist),500
            else:
                db.session.commit()
                return jsonify(success="All invitations sent successfully"),201
    except Exception as e:
        db.session.rollback()
        if isinstance(e,sqlalchemy.exc.IntegrityError):
            print e
            return jsonify(error="Something went wrong probably event does not exist or you the user has already been invited"),500
        else:
            print e
            log(e)
            return jsonify(error="Oops! something broke, we'll fix it soon."),500



@app.route('/<emailid>/pay/<eventid>',methods=["GET","POST"])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
@login_required
def pay_share(emailid,eventid):
    try:
        data=request.get_json(force=True)
        if current_user(data['authtoken'])==emailid:
            temp_eventid=eventid
            temp_emailid=emailid
            share = Invitee.query.get((str(temp_emailid),int(temp_eventid)))
            wallet = Wallet.query.get(emailid)
            if share is not None and share.transaction_id =='':
                if share.amount <= wallet.amount:
                    print "before makepayment"
                    makepayment(wallet,share)
                    print share.transaction_id
                    db.session.flush()
                    db.session.commit()
                    return jsonify(success="Your Payment Request has been submitted check status in payment history"),200
                else:
                    return jsonify(error="Insufficient Balance"),500
            else:
                return jsonify(error="You are not invited in this event or you have already paid your share"),403
        else:
            return jsonify(error="You are not authorised to make payment on other users behalf."),403
    except Exception as e:
        if isinstance(e,sqlalchemy.exc.IntegrityError):
            print e
            return jsonify(error="Some problem with sql constraints"),500
        else:
            log(e)
            return jsonify(error="Something went wrong"),500


@app.route('/<emailid>/wallet/add',methods=["GET","POST"])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
@login_required
def addtowallet(emailid):
    try:
        data=request.get_json(force=True)
        emailid=str(emailid)
        print emailid,current_user(data['authtoken'])
        if current_user(data['authtoken'])==emailid:
            wallet = Wallet.query.get(emailid)
            if wallet is not None:
                makepayment(wallet,amount=data['amount'])
                db.session.flush()
                db.session.commit()
                return jsonify(success="Your Payment Request has been submitted check status in payment history"),200
            else:
                return jsonify(error="You Have not registered for Wallet"),403
        else:
            return jsonify(error="You are not authorised to make payment on other users behalf."),403
    except Exception as e:
        if isinstance(e,sqlalchemy.exc.IntegrityError):
            print e
            return jsonify(error="Some problem with sql constraints"),500
        else:
            log(e)
            return jsonify(error="Something went wrong"),500


@app.route('/registry/create',methods=["POST"])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
@login_required
def create_registry():
    try:
        db.create_all()
        data=request.get_json(force=True)
        if current_user(data['authtoken'])!=data['email_id']:
            return jsonify(error="You are not authorised to create registry for this user"),403
        else:
            # import pdb
            # pdb.set_trace()
            db.create_all()
            if len(data['registry_name'])!=0:
                target_date=datetime.datetime.strptime(data['target_date'], "%d%m%Y").date()
                pool=Pool()
                db.session.add(pool)
                db.session.flush()
                registry=Registry(pool.pool_id,data['email_id'],data['registry_name'],target_date
                            ,data['description'])
                db.session.add(registry)
                db.session.flush()
                registry_id=registry.registry_id
                for pid in data['products']:
                    print registry.registry_id
                    giftbucket=GiftBucket(registry.registry_id,pid)
                    db.session.add(giftbucket)
                inviteSent=True
                failedlist=[]
                if "invites" in data:
                    for invite in data['invites']:
                        inviteentry=Invitee(invite['email_id'],registry.registry_id,0)
                        if not sendinvite(invite['email_id'],registry.email_id,registry.registry_name,data['msg']):
                            inviteSent=False
                            failedlist.append(invite['email_id'])
                        else:
                            db.session.add(inviteentry)
                            db.session.commit()
                else:
                    db.session.commit()
                return jsonify(success="Registry created successfully.",registry_id=registry_id,
                               failedlist=failedlist,inviteSent=inviteSent),201
            else:
                return jsonify(error="Registry name field empty"),500
    except Exception as e:
        if isinstance(e,sqlalchemy.exc.IntegrityError):
            db.session.rollback()
            print e
            return jsonify(error="Event already Exists or User does not exists"),500
        elif isinstance(e,KeyError):
            print e
            return jsonify(error="Please send all the required fields"),500

        else:
            print e
            log(e)
            db.session.rollback()
            return jsonify(error="Something went wrong!"),500


@app.route('/<email_id>/wallet/history',methods=["GET","POST"])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
@login_required
def transaction_hist(email_id):
    try:
        data=request.get_json(force=True)
        email_id=str(email_id)
        if current_user(data['authtoken'])==email_id:
            transactions = Transaction.query.filter_by(email_id=email_id)
            if transactions is not None:
                transactionlist=[]
                res={}
                for transaction in transactions:
                    res['transaction_id']=transaction.transaction_id
                    res['date']=str(transaction.date)
                    res['pool_id']=transaction.pool_id
                    res['amount']=transaction.amount
                    transactionlist.append(res.copy())
                return jsonify(transactions=transactionlist),200
            else:
                return jsonify(error="No transactions for this wallet"),403
        else:
            return jsonify(error="You are not authorised to view history for this wallet."),403
    except Exception as e:
        if isinstance(e,sqlalchemy.exc.IntegrityError):
            print e
            return jsonify(error="Some problem with sql constraints"),500
        else:
            log(e)
            return jsonify(error="Something went wrong"),500



@app.route('/')
# @cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
def test():
    db.create_all()
    return jsonify(success="It works")




__author__ = 'gaurav'













