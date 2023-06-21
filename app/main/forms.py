from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    post = TextAreaField('Squeak something', validators=[DataRequired()])
    submit = SubmitField('Squeak')


class NameForm(FlaskForm):
    name = StringField("What's your name?", validators=[DataRequired()])
    submit = SubmitField("Send")


class EditProfileForm(FlaskForm):
    about_me = TextAreaField('About me', validators=[Length(0, 160)])
    location = StringField('Location', validators=[Length(0, 64)])
    submit = SubmitField('Update profile')