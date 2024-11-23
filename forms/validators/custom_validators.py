from datetime import date

from wtforms.validators import ValidationError

"""
Validates date for birthday
birthday cannot be later than now
"""
class Birthday(object):
    def __init__(self, message=None):
        if not message:
            message = 'Birthday cannot be later than today.'
        self.message = message

    def __call__(self, form, field):
        form_date = field.data
        if form_date > date.today():
            raise ValidationError(self.message)

"""
Validates date for schedules
schedules cannot be in the past
"""
class ScheduleDate(object):
    def __init__(self, message=None):
        if not message:
            message = 'Schedule cannot be in the past'
        self.message = message

    def __call__(self, form, field):
        form_date = field.data
        if form_date < date.today():
            raise ValidationError(self.message)


"""
Validates start and end time for schedules
start has to be before end
"""
class ScheduleTime(object):
    def __init__(self, message=None):
        if not message:
            message = 'Schedule End Time cannot be earlier than Start Time'
        self.message = message

    def __call__(self, form, field):
        if field.data <= form.start_time.data:
            raise ValidationError(self.message)

"""
Validated filed that is mandatory when repeat is True
"""
class OptionalMandatory(object):
    def __init__(self, message=None):
        if not message:
            message = 'This argument is required when repeat is selected'
        self.message = message

    def __call__(self, form, field):
        if field.data is None and form.repeat.data in True:
            raise ValidationError(self.message)
