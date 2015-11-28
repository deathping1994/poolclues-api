from app import bcrypt, app
from flask.ext.cors import cross_origin
from flask import request
from models import *
from utilities import *
from sqlalchemy import and_
import sqlalchemy.exc

# @app.route('/fblogintest/<fbtoken>',methods=["GET","POST"])
# @cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
# def testloo(fbtoken):
#     r= requests.get("https://graph.facebook.com/v2.5/me?access_token="+fbtoken)
#     if "error" in r.content:
#         return False
#     else:
#         return True

@app.route('/fblogin',methods=["GET","POST"])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
def fblogin():
    data=request.get_json(force=True)
    user =User(data['first_name'],data['middle_name'],data['last_name'], data['email_id'],
               bcrypt.generate_password_hash(''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6)) +
                                                               str(datetime.datetime.now())),data['house_no'],data['street'],
               data['city'],data['state'],data['country'])
    try:
        if not tokenvalid(data['fbtoken']):
            return jsonify(error="Facebook login failed.Try Again"),403
        if "user_img" in data:
            user.user_img=data['user_img']
        res=User.query.get(data['email_id'])
        authtoken=bcrypt.generate_password_hash(user.email_id+str(datetime.datetime.now()))
        if res is None:
            db.session.add(user)
            # db.session.add(guest)
            db.session.flush()
            wallet=Wallet(user.email_id,0)
            db.session.add(wallet)
            db.session.commit()
            if "phone" in data:
                addphone(data['email_id'],data['phone'])
        if start_session(user.email_id,authtoken):
            return jsonify(success="Successfully Logged in !",authtoken=authtoken)
    except Exception as e:
        log(e)
        print e
        return jsonify(error="Oops something went wrong. Contact administrator"),500



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
        if "user_img" in data:
            user.user_img=data['user_img']
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
@cross_origin(origin='*', headers=["Content- Type", "Authorization"])
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




@app.route('/<email_id>/pool/list/<type>',methods=["POST","GET"])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
@login_required
def pool_list(email_id,type):
    try:
        data=request.get_json(force=True)
        email_id=str(email_id)
        type=str(type)
        if current_user(data['authtoken'])==email_id:
            if type=="contributed":
                sql="SELECT * FROM pool where pool_id IN (SELECT pool_id from contributor where email_id ='"+email_id+"' )"
            elif type=="created":
                sql="SELECT * FROM pool where email_id ='"+email_id+"'"
            elif type=="all":
                sql="SELECT * FROM pool where pool_id IN (SELECT pool_id from contributor where email_id ='"+email_id+"' ) or email_id= '"+email_id+"'"
            pools= db.engine.execute(sql)
            poollist=[]
            res={}
            if pools is not None:
                for pool in pools:
                    print pool.pool_id
                    res['pool_id']=pool.pool_id
                    res['pool_name']=pool.pool_name
                    res['target_date']=str(pool.target_date)
                    res['date_created']=str(pool.date_created)
                    res['target_amount']=pool.target_amount
                    res['pool_description']=pool.description
                    res['searchable']=pool.searchable
                    poollist.append(res.copy())
                print poollist
                return jsonify(pool_list=poollist),200
            else:
                return jsonify(error="No pools found"),500
        else:
            return jsonify(error="You are not authorised to view this pool list."),403
    except Exception as e:
        if isinstance(e,sqlalchemy.exc.SQLAlchemyError):
            print e
            return jsonify(error="Pool Does not exist or some other sqlalchemy error"),500
        else:
            log(e)
            print e
            return jsonify(error="Something went wrong!"),500


@app.route('/pool/<pool_id>',methods=["POST","GET"])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
@login_required
def display_pool(pool_id):
    try:
        data=request.get_json(force=True)
        curruser=current_user(data['authtoken'])
        flag=False
        pool= Pool.query.get(int(pool_id))
        if pool is None:
            return jsonify(error="Pool does not exist"),500
        if pool.email_id==curruser:
            flag=True
        contributors=Contributor.query.filter_by(pool_id=pool.pool_id)
        auth=contributors.filter_by(email_id=curruser)
        if auth is None:
            return jsonify(error="You are not a contributor in this pool"),403
        contributorlist=[]
        res={}
        for contributor in contributors:
            res['email_id']=contributor.email_id
            res['amount']=contributor.amount
            res['amount_paid']=contributor.amount_paid
            res['status']=contributor.status
            contributorlist.append(res.copy())
        return jsonify(is_creator=flag,pool_id=pool.pool_id,pool_name=pool.pool_name,target_date=str(pool.target_date),
                       target_amount=pool.target_amount,pool_description=pool.description,contributors=contributorlist),200
    except Exception as e:
        if isinstance(e,sqlalchemy.exc.SQLAlchemyError):
            return jsonify(error="some  sqlalchemy error"),500
        else:
            log(e)
            print e
            return jsonify(error="Something went wrong!"),500


@app.route('/pool/create',methods=["POST","GET"])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
@login_required
def create_pool():
    try:
        db.create_all()
        data=request.get_json(force=True)
        if current_user(data['authtoken'])!=data['email_id']:
            return jsonify(error="You are not authorised to create events for this user"),403
        else:
            # import pdb
            # pdb.set_trace()
            db.create_all()
            if len(data['pool_name'])!=0:
                target_date=datetime.datetime.strptime(data['target_date'], "%d%m%Y").date()
                event=Event()
                db.session.add(event)
                db.session.flush()
                print event.event_id
                pool=Pool(event.event_id,data['email_id'],data['pool_name'],target_date,data['target_amount'],data['description'])
                if "pool_img" in data:
                    pool.pool_img=data['pool_img']
                if "searchable" in data:
                    pool.searchable=data['searchable']
                db.session.add(pool)
                db.session.flush()
                pool_id=pool.pool_id
                if "products" in data:
                    for pid in data['products']:
                        giftbucket=GiftBucket(pool_id,pid)
                    db.session.add(giftbucket)
                else:
                    voucher_code=get_voucher_code(data['target_amount'])
                    giftbucket=GiftBucket(pool_id,voucher_code)
                    db.session.add(giftbucket)
                inviteSent=True
                failedlist=[]
                if "contributors" in data:
                    num = len(data['contributors'])
                    print num
                    if num<=1:
                        return jsonify(error="Atleast One Contributor other than user required"),500
                    for contributor in data['contributors']:
                        if "amount" in contributor:
                            contributorentry=Contributor(contributor['email_id'],pool_id,contributor['amount'])
                        else:
                            amount=float(pool.target_amount)/num
                            contributorentry=Contributor(contributor['email_id'],pool_id,amount)
                        if not sendinvite(contributor['email_id'],pool.email_id,pool.pool_name,data['msg']):
                            inviteSent=False
                            failedlist.append(contributor['email_id'])
                        else:
                            db.session.add(contributorentry)
                            db.session.commit()
                else:
                    db.session.rollback()
                    return jsonify(error="At least One Contributor other than user required"),500
                return jsonify(success="Pool created successfully.",pool_id=pool_id,
                               failedlist=failedlist,inviteSent=inviteSent),201
            else:
                return jsonify(error="Pool name field empty"),500
    except Exception as e:
        if isinstance(e,sqlalchemy.exc.IntegrityError):
            db.session.rollback()
            print e
            return jsonify(error="Pool already Exists or User does not exists"),500
        else:
            print e
            log(e)
            db.session.rollback()
            return jsonify(error="Something went wrong!"),500



@app.route('/pool/<pool_id>/contributor/add',methods=["POST","GET"])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
@login_required
def addcontributor(pool_id):
    try:
        pool_id= str(pool_id)
        data=request.get_json(force=True)
        pool= Pool.query.get(pool_id)
        if current_user(data['authtoken'])!=pool.email_id:
            return jsonify(error="You are not authorised to add contributors to this pool."),403
        else:
            inviteSent=True
            failedlist=[]
            if "contributors" in data:
                    num = len(data['contributors'])
                    for contributor in data['contributors']:
                        if "amount" in contributor:
                            contributorentry=Contributor(contributor['email_id'],pool_id,contributor['amount'])
                        else:
                            return jsonify(error="Please Provide Amount for each Contributor")
                        if not sendinvite(contributor['email_id'],pool.email_id,pool.pool_name,data['msg']):
                            inviteSent=False
                            failedlist.append(contributor['email_id'])
                        else:
                            db.session.add(contributorentry)
                            db.session.flush()
            if not inviteSent:
                return jsonify(error="Could not send out some invitations",failedlist=failedlist),500
            else:
                db.session.commit()
                return jsonify(success="All contributors invited successfully"),201
    except Exception as e:
        db.session.rollback()
        if isinstance(e,sqlalchemy.exc.IntegrityError):
            print e
            return jsonify(error="Something went wrong probably pool does not exist or the user has already been invited"),500
        else:
            print e
            log(e)
            return jsonify(error="Oops! something broke, we'll fix it soon."),500


@app.route('/<email_id>/<pool_id>/find/share',methods=["GET","POST"])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
@login_required
def find_share(email_id,pool_id):
    try:
        data=request.get_json(force=True)
        email_id=str(email_id)
        if current_user(data['authtoken'])==email_id:
            temp_pool_id=pool_id
            temp_email_id=email_id
            share = Contributor.query.get((str(temp_email_id),int(temp_pool_id)))
            if share is not None:
                if share.status == "REJECTED":
                    return jsonify(error="You rejected the invitation to contribute to this pool"),500
                else:
                    return jsonify(amount=share.amount,amount_paid=share.amount_paid),200
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


@app.route('/<email_id>/pay/<pool_id>',methods=["GET","POST"])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
@login_required
def pay_share(email_id,pool_id):
    try:
        data=request.get_json(force=True)
        email_id=str(email_id)
        if current_user(data['authtoken'])==email_id:
            temp_pool_id=pool_id
            temp_email_id=email_id
            share = Contributor.query.get((str(temp_email_id),int(temp_pool_id)))
            wallet = Wallet.query.get(email_id)
            if share is not None:
                if share.amount <= wallet.amount:
                    print "before makepayment"
                    makepayment(wallet,share)
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
                event=Event()
                db.session.add(event)
                db.session.flush()
                registry=Registry(event.event_id,data['email_id'],data['registry_name'],target_date
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
                        inviteentry=Invitee(invite['email_id'],registry.registry_id)
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


@app.route('/<email_id>/pool/<pool_id>/delete',methods=["POST"])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
@login_required
def delete_pool(email_id,pool_id):
    try:
        data=request.get_json(force=True)
        email_id=str(email_id)
        pool_id=str(pool_id)
        print email_id,pool_id
        if current_user(data['authtoken'])!=email_id:
            return jsonify(error="You are not authorised to delete this pool"),403
        else:
            reg=Pool.query.get(pool_id)
            if reg is not None:
                db.session.delete(reg)
                refund()
                db.session.commit()
                return jsonify(error="Pool deleted Successfully"),204
            else:
                return jsonify(error="Pool Does not exist"),404
    except Exception as e:
        if isinstance(e,sqlalchemy.exc.IntegrityError):
            db.session.rollback()
            print e
            return jsonify(error="Something wrong with sql alchemy"),500
        else:
            print e
            log(e)
            db.session.rollback()
            return jsonify(error="Something went wrong!"),500


@app.route('/<email_id>/pool/<pool_id>/update',methods=["POST"])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
@login_required
def update_pool(email_id,pool_id):
    try:
        data=request.get_json(force=True)
        email_id=str(email_id)
        pool_id=str(pool_id)
        print email_id,pool_id
        if current_user(data['authtoken'])!=email_id:
            return jsonify(error="You are not authorised to modify this pool"),403
        else:
            reg=Pool.query.get(pool_id)
            if reg is not None:
                if "pool_name" in data:
                    reg.pool_name=data['pool_name']
                if 'target_date' in data:
                    target_date=datetime.datetime.strptime(data['target_date'], "%d%m%Y").date()
                    if target_date>datetime.datetime.utcnow():
                        reg.target_date=target_date
                    else:
                        return jsonify(error="New date can't be in past"),500
                if 'target_amount' in data:
                    if data['target_amount'] > reg.target_amount:
                        reg.target_amount=data['target_amount']
                    else:
                        return jsonify(error="You can't reduce the target amount"),500
                if 'description' in data:
                    reg.description=data['description']
                if 'searchable' in data:
                    reg.searchable=data['searchable']
                db.session.commit()
                return jsonify(error="Pool Updated Successfully"),204
            else:
                return jsonify(error="Pool Does not exist"),404
    except Exception as e:
        if isinstance(e,sqlalchemy.exc.IntegrityError):
            db.session.rollback()
            print e
            return jsonify(error="Something wrong with sql alchemy"),500
        else:
            print e
            log(e)
            db.session.rollback()
            return jsonify(error="Something went wrong!"),500

@app.route('/<email_id>/registry/list',methods=["POST","GET"])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
@login_required
def registry_list(email_id):
    try:
        data=request.get_json(force=True)
        email_id=str(email_id)
        curruser=current_user(data['authtoken'])
        print curruser
        auth=Invitee.query.filter_by(email_id=curruser)
        if auth is None:
            return jsonify(error="No Registry"),404
        else:
            sql="SELECT * FROM registry where registry_id IN (SELECT registry_id from invitee where email_id ='"+curruser+"' ) "
        print str(sql)
        pools= db.engine.execute(sql)
        poollist=[]
        res={}
        if pools is not None:
            for pool in pools:
                print pool.registry_id
                res['pool_id']=pool.registry_id
                res['pool_name']=pool.registry_name
                res['target_date']=str(pool.target_date)
                res['date_created']=str(pool.date_created)
                res['pool_description']=pool.description
                res['searchable']=pool.searchable
                poollist.append(res.copy())
            print poollist
            return jsonify(registry_list=poollist),200
        else:
            return jsonify(error="No pools found"),500
    except Exception as e:
        if isinstance(e,sqlalchemy.exc.SQLAlchemyError):
            print e
            return jsonify(error="Pool Does not exist or some other sqlalchemy error"),500
        else:
            log(e)
            print e
            return jsonify(error="Something went wrong!"),500


@app.route('/registry/<registry_id>',methods=["POST","GET"])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
@login_required
def display_registry(registry_id):
    try:
        data=request.get_json(force=True)
        curruser=current_user(data['authtoken'])
        flag=False
        registry= Registry.query.get(int(registry_id))
        if registry is None:
            return jsonify(error="Registry does not exist"),500
        if registry.email_id==curruser:
            flag=True
        invitee=Invitee.query.filter_by(registry_id=registry.registry_id)
        auth=invitee.filter_by(email_id=curruser)
        if registry.searchable!=True:
            if auth is None:
                return jsonify(error="This registry is not shared with you"),403
        inviteelist=[]

        for invite in invitee:
            inviteelist.append(invite.email_id)
        giftbucket=GiftBucket.query.filter_by(event_id=registry.registry_id,)
        giftlist=[]
        res={}
        for gift in giftbucket:
            res['pid']= gift.product_id
            res['status']= gift.status
            if gift.status=="pooling":
                res['pool_id']= gift.pool_id
            giftlist.append(res.copy())

        return jsonify(is_creator=flag,registry_id=registry.registry_id,registry_name=registry.registry_name,
                       target_date=str(registry.target_date),
                       registry_description=registry.description,invitees=inviteelist,giftbucket=giftlist),200
    except Exception as e:
        if isinstance(e,sqlalchemy.exc.SQLAlchemyError):
            print str(e)
            return jsonify(error="some  sqlalchemy error"),500
        else:
            log(e)
            print e
            return jsonify(error="Something went wrong!"),500


@app.route('/registry/<registry_id>/invite',methods=["POST","GET"])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
@login_required
def registry_invite(registry_id):
    try:
        registry_id=str(registry_id)
        data=request.get_json(force=True)
        registry= Registry.query.get(int(registry_id))
        if current_user(data['authtoken'])!=registry.email_id:
            return jsonify(error="You are not authorised to send invites for this Registry."),403
        else:
            inviteSent=True
            failedlist=[]
            for invite in data['invites']:
                inviteentry=Invitee(invite['email_id'],registry.registry_id)
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


@app.route('/<email_id>/registry/<registry_id>/update',methods=["POST"])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
@login_required
def update_registry(email_id,registry_id):
    try:
        data=request.get_json(force=True)
        email_id=str(email_id)
        registry_id=str(registry_id)
        if current_user(data['authtoken'])!=email_id:
            return jsonify(error="You are not authorised to modify this registry"),403
        else:
            reg=Registry.query.get(registry_id)
            if reg is not None:
                if "registry_name" in data:
                    reg.name=data['registry_name']
                if 'target_date' in data:
                    target_date=datetime.datetime.strptime(data['target_date'], "%d%m%Y").date()
                    if target_date>datetime.datetime.utcnow():
                        reg.target_date=target_date
                    else:
                        return jsonify(error="New date can't be in past"),500
                if 'description' in data:
                    reg.description=data['description']
                if 'searchable' in data:
                    reg.searchable=data['searchable']
                db.session.commit()
                return jsonify(error="Registry Updated Successfully"),204
            else:
                return jsonify(error="Registry Does not exist"),404
    except Exception as e:
        if isinstance(e,sqlalchemy.exc.IntegrityError):
            db.session.rollback()
            print e
            return jsonify(error="Something wrong with sql alchemy"),500
        else:
            print e
            log(e)
            db.session.rollback()
            return jsonify(error="Something went wrong!"),500


@app.route('/<email_id>/registry/<registry_id>/delete',methods=["POST"])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
@login_required
def delete_registry(email_id,registry_id):
    try:
        data=request.get_json(force=True)
        email_id=str(email_id)
        registry_id=str(registry_id)
        print email_id,registry_id
        if current_user(data['authtoken'])!=email_id:
            return jsonify(error="You are not authorised to create delete this registry"),403
        else:
            reg=Registry.query.get(registry_id)
            if reg is not None:
                db.session.delete(reg)
                db.session.commit()
                return jsonify(error="Registry deleted Successfully"),204
            else:
                return jsonify(error="Registry Does not exist"),404
    except Exception as e:
        if isinstance(e,sqlalchemy.exc.IntegrityError):
            db.session.rollback()
            print e
            return jsonify(error="Something wrong with sql alchemy"),500
        else:
            print e
            log(e)
            db.session.rollback()
            return jsonify(error="Something went wrong!"),500


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


@app.route('/<email_id>/wallet',methods=["GET","POST"])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
@login_required
def wallet_amount(email_id):
    try:
        data=request.get_json(force=True)
        email_id=str(email_id)
        if current_user(data['authtoken'])==email_id:
            wallet = Wallet.query.get(email_id)
            if wallet is not None:
                return jsonify(amount=wallet.amount),200
            else:
                return jsonify(error="You have not registered for a wallet"),403
        else:
            return jsonify(error="You are not authorised to view this wallet."),403
    except Exception as e:
        if isinstance(e,sqlalchemy.exc.IntegrityError):
            print e
            return jsonify(error="Some problem with sql constraints"),500
        else:
            log(e)
            return jsonify(error="Something went wrong"),500


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


















