from flask_wtf import FlaskForm
from wtforms import HiddenField, SelectField, DateTimeLocalField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Optional
from models.enums.vaccination_type import VaccinationType

class EditExaminationForm(FlaskForm):
    animal_id = SelectField('Animal ID', coerce=int, validators=[DataRequired()], choices=[])
    date = DateTimeLocalField('Date and Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    type = SelectField('Type',
                       choices=[('examination', 'Examination'), ('vaccination', 'Vaccination'), ('preventive_checkup', 'Preventive CheckUp')],
                       validators=[DataRequired()])
    vaccination_type = SelectField('Vaccination Type',
                                    choices=[(vaccination.name, vaccination.value) for vaccination in VaccinationType],
                                    validators=[Optional()])
    description = TextAreaField('Description', validators=[Optional()])

    submit = SubmitField('Update')
    delete = SubmitField('Delete') 
