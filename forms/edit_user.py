from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length
from forms.validators.custom_validators import OnlyAlphabets

class EditUserForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired(), Length(min=2, max=20)])
    first_name = StringField('First Name', validators=[DataRequired(), OnlyAlphabets, Length(min=1, max=30)])
    last_name = StringField('Last Name', validators=[DataRequired(), OnlyAlphabets, Length(min=1, max=30)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    role = SelectField('Role', 
                       choices=[
                           ('admin', 'Admin'),
                           ('caretaker', 'Caretaker'),
                           ('vet', 'Vet'),
                           ('volunteer', 'Volunteer')
                       ],
                       validators=[DataRequired()])
    
    submit = SubmitField('Save')
    cancel = SubmitField('Cancel')
    delete = SubmitField('Delete')
    