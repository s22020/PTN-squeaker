import os
from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'changeit'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

bootstrap = Bootstrap(app)
moment = Moment(app)

posts = []

@app.route("/", methods=["GET", "POST"])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if User is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('user.html', form=form, name=session.get('name'))


@app.route("/post", methods=["GET", "POST"])
def post():
    form = PostForm()
    user = User.query.filter_by(username=session.get('name')).first()
    posts = Post.query.filter_by(user=user).all()
    if user is not None:
        print(user)
        if form.validate_on_submit():
            post = Post(post=(form.post.data.strip()))
            db.session.add(post)
            db.session.commit()
            form.post.data = ''
            return redirect(url_for('post'))
    return render_template('post.html', form=form, posts=posts, name=session.get('name'), current_time=datetime.utcnow())


@app.errorhandler(404)
def not_found(e):
    return render_template('not_found.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500



class PostForm(FlaskForm):
    post = TextAreaField('Squeak something', validators=[DataRequired()])
    submit = SubmitField('Squeak')


class NameForm(FlaskForm):
    name = StringField("What's your name?", validators=[DataRequired()])
    submit = SubmitField("Send")

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    posts = db.relationship('Post', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.username


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.String(140), index=True, nullable=False)
    likes = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Post %r>' % self.post


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Post=Post)