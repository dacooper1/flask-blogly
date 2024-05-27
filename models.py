"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.String(20), nullable=False)

    last_name = db.Column(db.String(20), nullable=False)

    image_url = db.Column(db.String)

    def __repr__(self):
        """Displaying User"""

        u = self 
        return f"<id={u.id}, first_name={u.first_name},last_name={u.last_name}, image_url={u.image_url}>"
    
class Post(db.Model):
    
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String(20), nullable=False)

    content = db.Column(db.String, nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    # date_time = db.Column(db.DateTime(timezone=True))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        """Displaying User"""

        u = self 
        return f"<id={u.id}, title={u.first_name},last_name={u.title}, content={u.content}>"
    
    user = db.relationship('User', backref='posts')
    
    