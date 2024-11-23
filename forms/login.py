from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from forms.validators.custom_validators import OnlyAlphabets

class LoginForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired(), OnlyAlphabets, Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=3, max=30)])
    submit = SubmitField('Log In')
