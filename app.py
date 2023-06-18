from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'changeit'

bootstrap = Bootstrap(app)
moment = Moment(app)

posts = []

@app.route("/", methods=["GET", "POST"])
def index():
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('user.html', form=form, name=session.get('name'))


@app.route("/post", methods=["GET", "POST"])
def post():
    form = PostForm()
    if form.validate_on_submit():
        posts.append(form.squeak.data.strip())
        return redirect(url_for('post'))
    return render_template('post.html', form=form, posts=posts, name=session.get('name'), current_time=datetime.utcnow())


@app.errorhandler(404)
def not_found(e):
    return render_template('not_found.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500



class PostForm(FlaskForm):
    squeak = TextAreaField('Squeak something', validators=[DataRequired()])
    submit = SubmitField('Squeak')


class NameForm(FlaskForm):
    name = StringField("What's your name?", validators=[DataRequired()])
    submit = SubmitField("Send")