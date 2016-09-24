from flask import render_template, request
from app import app
from app.db import db
from app.dbmodels import User
from app.util import validate_table, getsalt, createhash

register_form = ['username', 'email', 'password', 'confirm-password']
login_form = ['username', 'password']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        if validate_table(login_form, request.form):

            username = request.form['username']
            password = request.form['password']     

            try:
                user_exists = User.query.filter_by(uname=username).first()
            except:
                user_exists = None

            if user_exists:
                if createhash(user_exists.salt,password) == user_exists.password:
                    return 'Login successful'

            return 'Login POST'
        else:
            return 'Bad Login POST request arguments.'
    else:
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        if validate_table(register_form, request.form):

            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            confirm = request.form['confirm-password']

            if password != confirm:
                #Add template logic for invalid registration.
                render_template('login.html')

            salt = getsalt()
            passhash = createhash(salt, password)
            newUser = User(username, email, salt, passhash)
            db.session.add(newUser)
            db.session.commit()
            return 'Register POST' 
        else:
            return 'Bad Register POST request arguments.'
    else:
        return render_template('login.html')