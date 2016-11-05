from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, current_user, login_required, logout_user
from . import auth
from .. import db
from ..models import User
from .forms import LoginForm, RegistrationForm

@auth.before_app_request 				# runs before every request
def before_request():
	if current_user.is_authenticated:
		current_user.ping()
		# if not current_user.confirmed and request.endpoint[:5] != 'auth.':
		# 	return redirect(url_for('auth.unconfirmed'))

@auth.route('/login', methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			# flash('assas')
			login_user(user, form.remember_me.data)
			return redirect(request.args.get('next') or url_for('main.index'))
		flash('Invalid username/password.')
	return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have been logged out.')
	return redirect(url_for('main.index'))

@auth.route('/register', methods = ['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User( username=form.username.data,
					email=form.email.data,
					password=form.password.data
			)
		db.session.add(user)
		flash('You can now login')
		return redirect(url_for('auth.login'))
	return render_template('auth/register.html', form = form)