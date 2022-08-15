from flask import render_template, request, redirect, session
from flask_app import app
from flask import flash
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return redirect ('/register')

@app.route('/register')
def register():
    return render_template('login_register.html')

    
@app.route('/create_user', methods=['POST'])
def create_user():
    if not User.validate_user(request.form):
        return redirect('/register')
    if not User.user_exist(request.form):
        return redirect('/register')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": pw_hash
    }
    id = User.save(data)
    session['user_id'] = id
    return redirect('/home')

@app.route('/login', methods=['POST'])
def login():
    data = {
        "email": request.form["email"]
    }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect('/register')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/register')
    session['user_id'] = user_in_db.id
    return redirect('/home')

@app.route('/home')
def welcome():
    if 'user_id' not in session:
        return redirect('/register')
    data = {
        'id': session['user_id']
    }
    return render_template("home.html", user=User.get_one(data), recipes=Recipe.get_all_recipes())

@app.route('/logout')
def logout_user():
    session.clear()
    return redirect('/register')