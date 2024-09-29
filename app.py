"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
app.app_context().push()
# db.drop_all()
db.create_all()

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

"""USER ROUTES"""

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
    image = request.form['image'] if request.form['image'] else "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png"
    print(f'Image Url:{request.form['image']}')
    new_user = User(first_name=fname, last_name=lname, image_url=image)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/")

@app.route("/users/<int:user_id>")
def user_details(user_id):
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user.id).all()

    return render_template("user_details.html", user=user, posts=posts)
    
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


"""POST ROUTES"""

@app.route("/users/<int:user_id>/posts/new")
def show_post_form(user_id):
    user = User.query.get_or_404(user_id)
    tags  = Tag.query.all()
    return render_template("create_post.html", user=user, tags=tags)

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def create_post(user_id):
    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    current_user_id = user.id
    title = request.form['title']
    content = request.form['content']

    new_post = Post(title=title, content=content, user_id=current_user_id, tags=tags)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")


@app.route("/posts/<int:post_id>")
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    # user = User.query.get_or_404(user_id)

    return render_template("post_details.html", post=post)


@app.route("/posts/<int:post_id>/edit")
def show_edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    user = post.user.id
    tags = Tag.query.all()
    print("0000000000000000000")
    print(user)
    return render_template("edit_post.html", post=post, user=user, tags=tags)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form ['content']
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    db.session.delete(post)
    db.session.commit()

    return redirect("/")


"""TAG ROUTES """

@app.route("/tags")
def list_tags():
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)



@app.route("/tags/<int:tag_id>")
def tag_details(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag_details.html', tag=tag)


@app.route("/tags/new")
def new_tag_form():
    posts = Post.query.all()
    return render_template('create_tag.html', posts=posts)


@app.route("/tags/new", methods=["POST"])
def create_tag():
    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(tag)
    db.session.commit()

    return redirect("/users")


@app.route("/tags/<int:tag_id>/edit")
def edit_tag_form(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('edit_tag.html', tag=tag, posts=posts)
# **POST */tags/[tag-id]/edit :*** Process edit form, edit tag, and redirects to the tags list.

@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")

@app.route('/tags/<int:tag_id>/delete', methods=["POST"] )
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect("/tags")