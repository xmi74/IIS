from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.validators import Length, DataRequired, Optional


class EditRequest(FlaskForm):
    title = SelectField(
        'Title',
        choices=[
            ('Examination', 'Examination'),
            ('Vaccination', 'Vaccination'),
            ('Preventive CheckUp', 'Preventive CheckUp')
        ],
        validators=[DataRequired()]
    )
    description = StringField('Description', validators=[Length(min=0, max=255)])

    submit = SubmitField('Save')
    delete = SubmitField('Delete')