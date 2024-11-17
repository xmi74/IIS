from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, NumberRange, StopValidation


def date_validate(form, form_date):
    if form_date.data > date.today():
        raise StopValidation('Date of birth cannot be in the future')

class EditAnimalForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    species = StringField('Species', validators=[DataRequired(), Length(min=2, max=50)])
    weight = IntegerField('Weight', validators=[DataRequired(),NumberRange(min=0)])
    birth_date = DateField('Birth Date', validators=[DataRequired(), date_validate])
    photo = StringField('Photo', validators=[])

    submit = SubmitField('Save')
    cancel = SubmitField('Cancel')
    delete = SubmitField('Delete')
