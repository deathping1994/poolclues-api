from app import mongo,bcrypt,db
import datetime
from flask import jsonify,request
import requests
from functools import wraps
import string,random


def get_voucher_code(amount):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6))


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        data = request.get_json(force=True)
        if 'authtoken' not in data:
            return jsonify(error="You need to send authtoken along with every request"),403
        if not check_status(data['authtoken']):
            return jsonify(error="Login Required"),403
        return f(*args, **kwargs)
    return decorated_function


def sendmail(to,message,subject):
    try:
        data={'to':to,
              'subject':subject,
              'message':message,
              "token":"$2b$12$8/Z.2WDlk9VVWVND/DVtgej5z.pxKakZYSfkGdLQCIy7VCXgm8VNm"
              }
        print data
        r= requests.post("http://128.199.169.129:8080/mailer/561e7e12a4fabe0943650ca2",json=data)
        print r.json()
        return True
    except Exception as e:
        raise e


def password_change_request(user,rid):
    try:
        mongo.db.password_change_requests.create_index("time",expireAfterSeconds=24*60)
        message="Your password reset request was received, your request Id is "+ rid +".\n Change your password by visiting this URL.\n" + "http://localhost/forgotpassword"
        if sendmail(user,message,"Forgot Password Request"):
            res=mongo.db.password_change_requests.update({"user" : user}, {"$set" : {"rid":rid,"time":datetime.datetime.utcnow()}},upsert=True)
            return True
        else:
            return False
    except Exception as e:
        print e
        log(e)
        return jsonify(error="Something went wrong."),500


def check_status(authtoken):
    res= mongo.db.session.find_and_modify({'authtoken': authtoken},{"$set":{"loggedat":datetime.datetime.utcnow()}})
    if res is not None:
        return True
    else:
        return False

def send_verification_email(user):
    try:
        verification_code=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6))
        message= "Verify your account by entering this verification code " + verification_code + "\n This code will expire after 24 hrs"
        mongo.db.verification_code.create_index("time",expireAfterSeconds=24*60)
        if sendmail(user,message,"Successfully Registered on Poolclues"):
            res=mongo.db.verification_code.update({"user" : user}, {"$set" : {"verification_code":verification_code,"time":datetime.datetime.utcnow()}},upsert=True)
            return True
        else:
            return False
    except Exception as e:
        print e
        log(e)
        return jsonify(error="Something went wrong."),500


def current_user(authtoken):
    curruser=mongo.db.session.find_one({'authtoken': authtoken})
    if curruser is not None:
        return curruser['user']
    else:
        return "NULL"


def sendinvite(to,fromemail,eventname,msg):
    message="Hi, "+fromemail+" has invited you to pool for "+eventname+ " on poolclues." +"\n"+msg
    print message
    subject= "Invitation for pooling"
    if not sendmail(to,message,subject):
        return False
    else:
        return True


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
        print data
        print mongo.db.poolclueslog.insert(data)
    except Exception:
        return jsonify(error="This time something seriously went wrong event log server is down"),500


def makepayment(wallet,share=None,amount=None):
    try:
        if share is not None:
            print wallet.amount,wallet.email_id
            print share.amount,share.event_id
            wallet.amount=wallet.amount-share.amount
            share.transaction_id=bcrypt.generate_password_hash(''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6)) +
                                                               str(datetime.datetime.now()))
            print share.transaction_id
        elif amount is not None:
            wallet.amount=wallet.amount + amount
            db.session.add(wallet)
            db.session.commit()
    except Exception as e:
        raise e
