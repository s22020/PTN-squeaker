from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
import jwt
import hashlib
from datetime import datetime, timedelta
from flask import current_app, request

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(128))
    location = db.Column(db.String(64))
    about_me = db.Column(db.String(160))
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    avatar_hash = db.Column(db.String(32))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = self.gravatar_hash()

    @property
    def password(self):
        raise AttributeError("Cannot read password")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha512', salt_length=16)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_password_reset_token(self):
        return jwt.encode({'reset_password': self.id, 'exp': datetime.utcnow() + timedelta(minutes=60)}, current_app.config['SECRET_KEY'], algorithm='HS512')

    @staticmethod
    def reset_password(token, new_password):
        try:
            decoded_token = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS512'])['reset_password']
        except:
            return False
        user = User.query.get(decoded_token)
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    def gravatar(self, size=100, default='retro', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.avatar_hash or self.gravatar_hash()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    def gravatar_hash(self):
        return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

    def __repr__(self):
        return '<User %r>' % self.username


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.String(140), index=True, nullable=False)
    likes = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Post %r>' % self.post


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))