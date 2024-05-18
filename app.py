"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
app.app_context().push()
db.create_all()

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

@app.route("/")
def homepage():
    return redirect("/users")

@app.route("/users")
def list_users():
    users = User.query.all()
    return render_template("list.html", users=users)

@app.route("/users/new")
def add_user():
    return render_template("create_user.html")

@app.route("/cancel")
def cancel_new_user():
    return redirect("/")

@app.route("/users/new", methods=["POST"])
def create_user():
    fname = request.form['fname']
    lname = request.form['lname']
    image = request.form['image'] if 'image' in request.form else "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png"
   
    new_user = User(first_name=fname, last_name=lname, image_url=image)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/")

@app.route("/users/<int:user_id>")
def user_details(user_id):
    user = User.query.get_or_404(user_id) 
    return render_template("user_details.html", user=user)
    
@app.route("/users/<int:user_id>/edit")
def edit_user(user_id):
    user = User.query.get_or_404(user_id) 
    return render_template("edit_user.html",  user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def update_user(user_id):

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['fname']
    user.last_name = request.form['lname']
    user.image_url = request.form['image'] 

    db.session.add(user)
    db.session.commit()

    return redirect("/")

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def  delete_user(user_id):
    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect("/")
