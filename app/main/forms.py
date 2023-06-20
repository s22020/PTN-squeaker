from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    post = TextAreaField('Squeak something', validators=[DataRequired()])
    submit = SubmitField('Squeak')


class NameForm(FlaskForm):
    name = StringField("What's your name?", validators=[DataRequired()])
    submit = SubmitField("Send")