from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'changeit'

bootstrap = Bootstrap(app)
moment = Moment(app)

posts = []

@app.route("/")
def index():
    return render_template('base.html')


@app.route("/user/<name>")
def user(name):
    return render_template('user.html', name=name)


@app.route("/post", methods=["GET", "POST"])
def post():
    form = PostForm()
    if form.validate_on_submit():
        posts.append(form.squeak.data)
        return redirect(url_for('post'))
    return render_template('post.html', form=form, posts=posts, current_time=datetime.utcnow())


@app.errorhandler(404)
def not_found(e):
    return render_template('not_found.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500



class PostForm(FlaskForm):
    squeak = TextAreaField('Squeak something', validators=[DataRequired()])
    submit = SubmitField('Squeak')