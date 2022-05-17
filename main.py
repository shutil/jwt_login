from flask import Flask, jsonify, session, make_response, request
from flask_session import Session
from dotenv import load_dotenv
import os
import jwt
import time

# create a login system with jwt
app = Flask(__name__)

load_dotenv(os.getcwd()+'/.config.env')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SESSION_COOKIE_SAMESITE'] = os.getenv('SESSION_COOKIE_SAMESITE')
app.config['SESSION_TYPE'] = os.getenv('SESSION_TYPE')

sess = Session(app)

@app.route("/")
def index():
    return jsonify({'api':'cookie is been set'})

@app.route("/login",methods=["POST"])
def login_route():
    if 'is_login' in session is not None:
        return jsonify({'error':'session is already set'})
    else:
        session['is_login'] = True
        return jsonify({'api':'ok'})

@app.route("/jwt",methods=["POST"])
def sc():
    if 'is_login' in session is not None:
        res = make_response({'api':'set cookie in your browser'})
        res2 = make_response({'api':'new token setted'})
        secret = app.config['SECRET_KEY']
        payload = {'username':"gitik",'exp':time.time()+30}
        
        if request.cookies.get('username') is None:
            # adding jwt
            token = jwt.encode(payload,secret,algorithm="HS256")
            res.set_cookie('username',token,samesite="Lax")
            return res
        else:
            # check jwt is expired or not
            try:
                decode = jwt.decode(request.cookies.get('username'),secret,algorithms=["HS256"])
            except jwt.ExpiredSignatureError as e:
                print("token expire")
                # generate new jwt
                payload = {'username':"john doe",'exp':time.time()+30}
                token = jwt.encode(payload,secret,algorithm="HS256")
                res2.set_cookie('username',token,samesite="Lax")
                return res2
            except jwt.InvalidTokenError as e:
                print("invalid token error")
                # generate new jwt
                payload = {'username':"john doe",'exp':time.time()+30}
                token = jwt.encode(payload,secret,algorithm="HS256")
                res2.set_cookie('username',token,samesite="Lax")
                return res2
            return jsonify({'error':'cookie is already set'})
    else:
        return jsonify({'error':'You are not logged in'})

@app.route("/logout",methods=["POST"])
def lgo():
    res = make_response({'api':'you are logged out now'})
    if 'is_login' in session is not None:
        session.pop('is_login',None)
        res.set_cookie('username',samesite='Lax',expires=0)
        return res
    else:
        return jsonify({'err':'You are not logged in'})

if __name__ == "__main__":
    app.run(debug=True,port=8000,ssl_context=('cert_file.pem','key_file.pem'))