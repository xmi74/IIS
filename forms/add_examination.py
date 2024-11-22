from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateTimeLocalField, TextAreaField, SubmitField, DateField
from wtforms.validators import DataRequired, Optional
from models.enums.vaccination_type import VaccinationType

class AddExaminationForm(FlaskForm):
    animal_id = StringField('Animal ID', validators=[DataRequired()])
    date = DateTimeLocalField('Date and Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()]) # format?
    type = SelectField('Type', 
                       choices=[('examination', 'Examination'), ('vaccination', 'Vaccination'), ('preventive_checkup', 'Preventive CheckUp')], 
                       validators=[DataRequired()])
    vaccination_type = SelectField('Vaccination Type',
                                  choices=[(vaccination.name, vaccination.value) for vaccination in VaccinationType],
                                  validators=[Optional()])
    description = TextAreaField('Description', validators=[Optional()])
    submit = SubmitField('Create')