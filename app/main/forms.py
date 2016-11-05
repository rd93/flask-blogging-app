from flask_wtf import Form
from wtforms import StringField, SubmitField, StringField, TextAreaField
from wtforms.validators import Required, Length, Regexp, Email, EqualTo
from wtforms import ValidationError
from ..models import User

class EditProfileForm(Form):
	name = StringField('Name')
	location = StringField('Location')
	about_me = TextAreaField('About Me')
	submit = SubmitField('Submit')

class PostForm(Form):
	body = TextAreaField("What's on your mind?", validators=[Required()])
	submit = SubmitField('Submit')

