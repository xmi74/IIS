from random import choices

from wtforms import validators
from wtforms.fields.choices import SelectField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import BooleanField

from forms.edit_schedules import EditSchedules


class AddSchedule(EditSchedules):
    repeat = BooleanField('Repeat', default=False)
    interval = SelectField('Interval',
                           choices=[
                               ('day', 'Day'),
                               ('week', 'Week')
                           ])
    count = IntegerField('Count', default=1, validators=[validators.NumberRange(min=1, max=31)])