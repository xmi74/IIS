from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import TextAreaField, URLField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, URL

from forms.validators.custom_validators import Birthday
from models.enums.animal_species import Species


class EditAnimalForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    species = SelectField('Species',
                          validators=[DataRequired()],
                          choices=[data.value for data in Species]
                          )
    birth_date = DateField('Birth Date', validators=[DataRequired(), Birthday()])
    weight = IntegerField('Weight', validators=[ Optional(),NumberRange(min=0)], default=None)
    photo = URLField('Photo', validators=[Optional(), URL()])
    description = TextAreaField('Description', validators=[Optional(), Length(min=0, max=500)], default='No description')

    submit = SubmitField('Save')
    delete = SubmitField('Delete')
