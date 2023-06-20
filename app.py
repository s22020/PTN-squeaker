import os
from threading import Thread
from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['SQUEAKER_MAIL_SUBJECT_PREFIX'] = '[Squeaker]'
app.config['SQUEAKER_MAIL_SENDER'] = 'Squeaker Admin <' + os.environ.get('SQUEAKER_MAIL_SENDER') + '>'


db = SQLAlchemy(app)
migrate = Migrate(app, db)

bootstrap = Bootstrap(app)
moment = Moment(app)

mail = Mail(app)

@app.route("/", methods=["GET", "POST"])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
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
    posts = Post.query.all()
    if form.validate_on_submit():
        if user is not None:
            post = Post(post=form.post.data.strip(), user=user)
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
    email = db.Column(db.String(64), unique=True, nullable=False)
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



def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def make_email_thread(to, subject, template, **kwargs):
    msg = Message(app.config['SQUEAKER_MAIL_SUBJECT_PREFIX'] + subject,
                    sender=app.config['SQUEAKER_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thrd = Thread(target=send_async_email, args=[app, msg])
    thrd.start()
    return thrd