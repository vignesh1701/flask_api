from flask import Flask,render_template,request,jsonify,url_for,flash,redirect,make_response
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from datetime import datetime,timedelta
import jwt
from flask_cors import cross_origin,CORS


app=Flask(__name__)
app.config['SECRET_KEY']='vignesh1234'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# creates SQLALCHEMY object
db = SQLAlchemy(app)





class Users(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20))
    password=db.Column(db.String(20))
    mobile=db.Column(db.String(10))
    mail=db.Column(db.String(20))

    def __init__(self,username,password,mobile,mail):
        self.username=username
        self.password=password
        self.mail=mail
        self.mobile=mobile

    @classmethod
    def find_user(cls,user):
        return(Users.query.filter_by(username=user).first())

    def save(self):
        db.session.add(self)
        db.session.commit()

db.create_all()

def token_required(f):
    @wraps(f)
    def decorarted(*args,**kwargs):
        if('auth' in request.args):
            token=request.args.get('auth')
            print(token)
        data=jwt.decode({'alg':'HS256'},token,app.config['SECRET_KEY'])
        data=token
        current_user=User.query.filter_by(username=data['user'])
        return f(current_user,*args,**kwargs)
    return decorarted



@app.route('/',methods=['POST','GET'])
def home():
    if(request.method=='POST'):
        user=request.form.get('user')
        password=request.form.get('password')
        mail=request.form.get('mail')
        mobile=request.form.get('mobile')
        if(password==''):
            flash('Password field cannot be empty','error')
            return(render_template('registration.html'))
        if(Users.find_user(user)):
            return(render_template('registration.html',msg=user))
        else:
            u=Users(user,password,mail,mobile)
            u.save()
            flash('User registred, use login link to login','info')
            return(redirect(url_for('login')))
    return(render_template('registration.html'))

@app.route('/login',methods=['POST','GET'])
def login():
    if(request.method=='POST'):
        user=request.form.get('user')
        password=request.form.get('password')
        u=Users.find_user(user)
        if(u.username==user and u.password==password):
            token=jwt.encode({'user':u.username,
            'exp':datetime.utcnow() + timedelta(minutes = 30)},app.config['SECRET_KEY'])
            return make_response(jsonify({'token':token}))
        else:
            return make_response(jsonify({'message':'Invalid user name or password'}))
    return(render_template('login.html'))

@app.route('/details')
@token_required
def details(current_user):
    return f'HI {current_user.username}, your email address is {current_user.mail}'

@app.route('/api')
@cross_origin()
def cors():
    return make_response(jsonify({'message':'hi i am vignesh'}))

if(__name__=='__main__'):
    app.run(debug=True)