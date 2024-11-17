from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired, Length

class EditAnimalForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    species = StringField('Species', validators=[DataRequired(), Length(min=2, max=50)])
    weight = IntegerField('Weight', validators=[DataRequired()])
    birth_date = DateField('Birth Date', validators=[DataRequired()])
    photo = StringField('Photo', validators=[])

    submit = SubmitField('Save')
    cancel = SubmitField('Cancel')
    delete = SubmitField('Delete')
