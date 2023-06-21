from flask import render_template, redirect, request, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from ..models import User
from .forms import LoginForm, RegistrationForm, ForgotPasswordForm, ResetPasswordForm
from ..email import make_email_thread

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            session['name'] = user.username
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid username or password')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been successfully logged out')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account was created successfully. You may now login.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            token = user.generate_password_reset_token()
            make_email_thread(user.email, 'Reset password', 'auth/email/reset-password', user=user, token=token)
        flash('If the e-mail exists in our databases, the password reset token was sent to your e-mail account')
        return redirect(url_for('auth.reset_password'))
    return render_template('auth/forgot-password.html', form=form)


@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset(token):
    form = ResetPasswordForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash('Password was successfully changed')
            return redirect(url_for('auth.login'))
        else:
            flash('Invalid token or token expired')
            return redirect(url_for('auth.reset_password'))
    return render_template('auth/reset-password.html', form=form)
