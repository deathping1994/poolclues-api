from app import mongo
import datetime
from flask import jsonify


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
