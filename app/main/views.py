from datetime import datetime
from flask import render_template, session, redirect, url_for, current_app, flash
from . import main
from .. import db
from .forms import NameForm, PostForm, EditProfileForm
from ..models import User, Post
from flask_login import login_user, logout_user, login_required, current_user


@main.route("/", methods=["GET", "POST"])
def index():
    form = PostForm()
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            post = Post(post=form.post.data.strip(), author=current_user._get_current_object())
            db.session.add(post)
            db.session.commit()
        form.post.data = ''
        return redirect(url_for('.index'))
    return render_template('index.html', form=form, posts=posts)


@main.route("/post", methods=["GET", "POST"])
@login_required
def post():
    form = PostForm()
    user = User.query.filter_by(username=current_user.username).first()
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    if form.validate_on_submit():
        post = Post(post=form.post.data.strip(), user=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        form.post.data = ''
        return redirect(url_for('.post'))
    return render_template('post.html', form=form, posts=posts)

@main.route('/post/<int:id>')
def post_id(id):
    post = Post.query.get_or_404(id)
    return render_template('post-id.html', posts=[post])

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html', user=user, posts=posts)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.about_me = form.about_me.data
        current_user.location = form.location.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile was successfully updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit-profile.html', form=form)
