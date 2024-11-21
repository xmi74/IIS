from datetime import date

from flask_wtf import FlaskForm
from wtforms.fields.choices import SelectField
from wtforms.fields.datetime import DateField, TimeField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired

from forms.validators.custom_validators import ScheduleDate, ScheduleTime
from models.enums.schedule_state import ScheduleState


class EditSchedules(FlaskForm):
    date = DateField('Date', validators=[DataRequired(), ScheduleDate()], default=date.today)
    start_time = TimeField('Start Time', validators=[DataRequired()])
    end_time = TimeField('End Time', validators=[DataRequired(), ScheduleTime()])
    state = SelectField('State',
                        validators=[DataRequired()],
                        choices=[data.value for data in ScheduleState],
                        default=ScheduleState.FREE.value,
                        )

    submit = SubmitField('Save')
    delete = SubmitField('Delete')