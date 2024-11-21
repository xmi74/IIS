from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateTimeField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Optional
from models.enums.vaccination_type import VaccinationType

class AddExaminationForm(FlaskForm):
    date = DateTimeField('Date', validators=[DataRequired()]) # format?
    type = SelectField('Type', 
                       choices=[('examination', 'Examination'), ('vaccination', 'Vaccination'), ('preventive_checkup', 'Preventive CheckUp')], 
                       validators=[DataRequired()])
    vaccination_type = SelectField('Vaccination Type',
                                  choices=[(vaccination.name, vaccination.value) for vaccination in VaccinationType],
                                  validators=[Optional()])
    description = TextAreaField('Description', validators=[Optional()])
    submit = SubmitField('Create')