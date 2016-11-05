from flask import render_template, flash, redirect, request, make_response, url_for, current_app
from flask_login import login_required, current_user
from datetime import datetime
from . import main
from ..decorators import admin_required, permission_required
from ..models import Permission
from .forms import EditProfileForm, PostForm
from .. import db
from ..models import User, Post
# from flask_login import current_user


@main.route('/', methods=['GET', 'POST'])
def index():
	form = PostForm()
	if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
		post = Post(body=form.body.data, author=current_user._get_current_object())
		db.session.add(post)
		return redirect(url_for('.index'))
	page = request.args.get('page', 1, type=int)
	pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
		page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
	posts = pagination.items
	return render_template('index.html', form=form, posts=posts, pagination=pagination)

@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
	return "For administrators!"

@main.route('/moderator')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def for_moderators_only():
	return "For comment moderators!"

@main.route('/user/<username>')
def user(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		abort(404)
	page = request.args.get('page', 1, type=int)
	pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
		page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
	posts = pagination.items
	return render_template('user.html', user=user, posts=posts, pagination=pagination)

@main.route('/post/<int:id>')
def post(id):
	post = Post.query.get_or_404(id)
	return render_template('post.html', posts=[post])

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
	post = Post.query.get_or_404(id)
	
	if current_user != post.author and \
	not current_user.can(Permission.ADMINISTER):
		abort(403)
	form = PostForm()
	
	if form.validate_on_submit():
		post.body = form.body.data
		db.session.add(post)
		flash('The post has been updated.')
		return redirect(url_for('.post', id=post.id))
	form.body.data = post.body
	return render_template('edit_post.html', form=form)

@main.route('/edit-profile', methods = ['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfileForm()
	if form.validate_on_submit():
		current_user.name = form.name.data
		current_user.location = form.location.data
		current_user.about_me = form.about_me.data
		db.session.add(current_user._get_current_object())
		flash('Your profile has been updated.')
		return redirect(url_for('.user', username=current_user.username))
	form.name.data = current_user.name
	form.location.data = current_user.location
	form.about_me.data = current_user.about_me
	return render_template('edit_profile.html', form=form)

@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash('Invalid User')
		return redirect(url_for('.index'))
	
	if current_user.is_following(user):
		flash('You are already following this user.')
		return redirect(url_for('.user', username=username))
	
	current_user.follow(user)
	flash('You are now following %s.' % username)
	return redirect(url_for('.user', username=username))


@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash('Invalid User')
		return redirect(url_for('.index'))
	
	if not current_user.is_following(user):
		flash('You are not following this user.')
		return redirect(url_for('.user', username=username))
	
	current_user.unfollow(user)
	flash('You have unfollowed %s.' % username)
	return redirect(url_for('.user', username=username))

@main.route('/followers/<username>')
def followers(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash('Invalid User')
		return redirect(url_for('.index'))

	page = request.args.get('page', 1, type=int)
	pagination = user.followers.paginate( page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
				 error_out=False)
	follows = [{'user': item.follower, 'timestamp': item.timestamp} for item in pagination.items]

	return render_template('followers.html', user=user, title="Followers of",
	endpoint='.followers', pagination=pagination, follows=follows)

@main.route('/following/<username>')
def following(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash('Invalid User')
		return redirect(url_for('.index'))

	page = request.args.get('page', 1, type=int)
	pagination = user.followed.paginate( page, per_page=current_app.config['FLASKY_FOLLOWED_PER_PAGE'],
				 error_out=False)
	followed = [{'user': item.followed, 'timestamp': item.timestamp} for item in pagination.items]

	return render_template('following.html', user=user, title="Follows",
	endpoint='.followers', pagination=pagination, followed=followed)


	