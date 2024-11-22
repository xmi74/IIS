from random import choices

from wtforms.fields.choices import SelectField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import BooleanField
from wtforms.validators import NumberRange

from forms.edit_schedules import EditSchedules
from forms.validators.custom_validators import OptionalMandatory


class AddSchedule(EditSchedules):
    repeat = BooleanField('Repeat', default=False, validators=[OptionalMandatory()])
    interval = SelectField('Interval',
                           choices=[
                               ('day', 'Day'),
                               ('week', 'Week')
                           ])
    count = IntegerField('Count', default=1, validators=[NumberRange(min=1, max=31)])