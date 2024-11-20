from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, NumberRange

from forms.validators.custom_validators import Birthday


class EditAnimalForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    species = StringField('Species', validators=[DataRequired(), Length(min=2, max=50)])
    weight = IntegerField('Weight', validators=[DataRequired(),NumberRange(min=0)])
    birth_date = DateField('Birth Date', validators=[DataRequired(), Birthday()])
    photo = StringField('Photo', validators=[])

    submit = SubmitField('Save')
    delete = SubmitField('Delete')
