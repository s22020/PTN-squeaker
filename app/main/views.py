from datetime import datetime
from flask import render_template, session, redirect, url_for, current_app
from . import main
from .. import db
from .forms import NameForm, PostForm
from ..models import User, Post


@main.route("/")
def index():
    return render_template('user.html')


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

