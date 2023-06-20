from datetime import datetime
from flask import render_template, session, redirect, url_for, current_app
from . import main
from .. import db
from .forms import NameForm, PostForm
from ..models import User, Post


@main.route("/", methods=["GET", "POST"])
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
        return redirect(url_for('.index'))
    return render_template('user.html', form=form, name=session.get('name'))


@main.route("/post", methods=["GET", "POST"])
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
        return redirect(url_for('.post'))
    return render_template('post.html', form=form, posts=posts, name=session.get('name'), current_time=datetime.utcnow())

