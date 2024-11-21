from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange

from forms.validators.custom_validators import Birthday
from models.enums.animal_species import Species


class EditAnimalForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    species = SelectField('Species',
                          validators=[DataRequired()],
                          choices=[data.value for data in Species]
                          )
    weight = IntegerField('Weight', validators=[NumberRange(min=0)])
    birth_date = DateField('Birth Date', validators=[DataRequired(), Birthday()])
    photo = StringField('Photo', validators=[])
    description = TextAreaField('Description', validators=[Length(min=0, max=500)], default='No description')

    submit = SubmitField('Save')
    delete = SubmitField('Delete')
