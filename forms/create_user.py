from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class CreateUserForm(FlaskForm):
    # Common Fields
    login = StringField('Login', validators=[DataRequired(), Length(min=2, max=20)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=1, max=30)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=30)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    
    # Password Fields
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    
    # Role Selection
    role = SelectField('Role', 
                       choices=[
                           ('admin', 'Admin'),
                           ('caretaker', 'Caretaker'),
                           ('vet', 'Vet'),
                           ('volunteer', 'Volunteer')
                       ],
                       validators=[DataRequired()])
    
    # Submit Buttons
    submit = SubmitField('Save')
    cancel = SubmitField('Cancel')
