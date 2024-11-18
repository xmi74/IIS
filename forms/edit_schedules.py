from flask_wtf import FlaskForm
from wtforms.fields.choices import SelectField
from wtforms.fields.datetime import DateField, TimeField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired
from models.enums.schedule_state import ScheduleState


class EditSchedules(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    start_time = TimeField('Start Date', validators=[DataRequired()])
    end_time = TimeField('End Date', validators=[DataRequired()])
    state = SelectField('State',
                        validators=[DataRequired()],
                        choices=[data.value for data in ScheduleState]
                        )

    submit = SubmitField('Save')
    delete = SubmitField('Delete')