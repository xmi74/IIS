from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, SubmitField
from wtforms.validators import Length, DataRequired, Optional


class EditRequest(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=80)])
    description = StringField('Description', validators=[Length(min=0, max=255)])

    submit = SubmitField('Save')
    delete = SubmitField('Delete')