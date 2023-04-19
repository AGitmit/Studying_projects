from database_config import db
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

# junction/intermidiary table for many-to-many relationship between Users and itself
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

following = db.Table('following',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)


class Users(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(400), nullable=False)
    posts = db.relationship('Posts', backref='author', lazy=True)
    liked_posts = db.relationship('Posts', backref='liked_posts', lazy=True)
    followers = db.relationship(
        'Users', 
        secondary=followers,
        primaryjoin=(followers.c.followed_id == id),
        secondaryjoin=(followers.c.follower_id == id),
        backref=db.backref('followed_by', lazy='dynamic'), lazy='dynamic'
        )
    followed = db.relationship(
        'Users', 
        secondary=following,
        primaryjoin=(following.c.follower_id == id),
        secondaryjoin=(following.c.followed_id == id),
        backref=db.backref('following_users', lazy='dynamic'),
        lazy='dynamic'
    )
