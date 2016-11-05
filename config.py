import os
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
SQLALCHEMY_TRACK_MODIFICATIONS = True

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or '1234'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
	FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
	FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
	FLASKY_POSTS_PER_PAGE = 10
	FLASKY_FOLLOWED_PER_PAGE = 10
	FLASKY_FOLLOWERS_PER_PAGE = 10
	
	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	print basedir
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or\
		'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
	
class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
	'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
	'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,

	'default': DevelopmentConfig
}

# WTF_XSRF_ENABLED = True
# SECRET_KEY = '1234'

# OPENID_PROVIDERS = [
#     {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
#     {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
#     {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
#     {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
#     {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}
#     ]