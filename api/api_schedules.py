from datetime import timedelta, date, datetime
from sqlalchemy import or_, and_

from __init__ import db
from models.walk_schedule import WalkSchedule
from models.enums.schedule_state import ScheduleState
import pytz


#READ ONE
def get_schedule(schedule_id):
    return WalkSchedule.query.get(schedule_id)

#READ ALL MAY FILTER
def get_schedules(filters=None):
    gmt_tz = pytz.timezone("Europe/Prague")
    query = WalkSchedule.query
    if 'date' in filters and filters['date'] is not None:
        query = query.filter(WalkSchedule.date >= filters['date'])
    if 'start_time' in filters and filters['start_time'] is not None:
        query = query.filter(WalkSchedule.start_time <= filters['start_time'])
    if 'end_time' in filters and filters['end_time'] is not None:
        query = query.filter(WalkSchedule.end_time >= filters['end_time'])
    if 'animal_id' in filters and filters['animal_id'] is not None:
        query = query.filter(WalkSchedule.animal_id == filters['animal_id'])
    if 'state' in filters and filters['state'] is not None:
        query = query.filter(WalkSchedule.state == filters['state'])
    if 'upcoming' in filters and filters['upcoming'] is True:
        query = query.filter(
            or_(
                WalkSchedule.date > date.today(),
                and_(
                    WalkSchedule.date == date.today(),
                    WalkSchedule.end_time >= datetime.now(gmt_tz).time()
                )
            )
        )

    query = query.order_by(WalkSchedule.date, WalkSchedule.start_time)
    return query.all()

#READ SCHEDULES WITCH STATE FREE OR RESERVED FOR ONE ANIMAL
def get_incoming_animal_schedules(animal_id):
    gmt_tz = pytz.timezone("Europe/Prague")
    now = datetime.now(gmt_tz)
    return WalkSchedule.query.filter(
        WalkSchedule.animal_id == animal_id,
        db.or_(
            WalkSchedule.date > now.date(),  # Future dates
            db.and_(
                WalkSchedule.date == now.date(),  # Today's schedules
                WalkSchedule.start_time > now.time()  # Future times only
            )
        ),
        WalkSchedule.state.in_([
            ScheduleState.FREE.value,
            ScheduleState.RESERVED.value,
            ScheduleState.CONFIRMED.value
        ])
    ).order_by(WalkSchedule.date).all()

#DELETE
def delete_schedule(schedule_id):
    schedule = WalkSchedule.query.get(schedule_id)
    db.session.delete(schedule)
    db.session.commit()
    return schedule

#CREATE
def create_schedule(schedule):
    new_schedule = WalkSchedule(
        date=schedule.get('date'),
        start_time=schedule.get('start_time'),
        end_time=schedule.get('end_time'),
        animal_id=schedule.get('animal_id'),
        state=schedule.get('state'),
        caretaker_id=schedule.get('caretaker_id'),
    )
    db.session.add(new_schedule)
    db.session.commit()
    return new_schedule

#CREATE MULTIPLE
def create_multiple_schedules(data):
    schedule_date = data.get('date')
    for count in range(data.get('count') + 1):
        if data.get('interval') == 'day':
            data['date'] = schedule_date + timedelta(days=count)
        elif data.get('interval') == 'week':
            data['date'] = schedule_date + timedelta(weeks=count)

        create_schedule(data)


#EDIT
def edit_schedule(id, new_schedule):
    schedule = WalkSchedule.query.get_or_404(id)
    schedule.date = new_schedule.get('date')
    schedule.start_time = new_schedule.get('start_time')
    schedule.end_time = new_schedule.get('end_time')
    schedule.state = new_schedule.get('state')
    schedule.volunteer_id = new_schedule.get('volunteer_id')

    try:
        db.session.commit()
    except Exception as e:
        print(f"Error commiting to database: {str(e)}")
        raise
    return schedule


def reserve_schedule(schedule_id, user_id):
    schedule = WalkSchedule.query.get(schedule_id)
    if schedule and schedule.state == ScheduleState.FREE.value:
        schedule.state = ScheduleState.RESERVED.value
        schedule.volunteer_id = user_id
        db.session.commit()
        return True
    return False

def get_volunteer_schedules(volunteer_id):
    return WalkSchedule.query.filter_by(volunteer_id=volunteer_id).order_by(WalkSchedule.date, WalkSchedule.start_time).all()

def get_closest_schedule(volunteer_id):
    schedules = get_volunteer_schedules(volunteer_id)
    gmt_tz = pytz.timezone("Europe/Prague")
    now = datetime.now(gmt_tz)

    for schedule in schedules:
        start_datetime = datetime.combine(schedule.date, schedule.start_time)
        end_datetime = datetime.combine(schedule.date, schedule.end_time)

        if start_datetime <= now <= end_datetime:
            return schedule  # Ongoing schedule
        elif start_datetime > now:
            return schedule  # Nearest upcoming schedule

    return None  # No ongoing or upcoming schedules

def get_past_schedules(volunteer_id):
    gmt_tz = pytz.timezone("Europe/Prague")
    now = datetime.now(gmt_tz)
    schedules = get_volunteer_schedules(volunteer_id)
    return [
        s for s in schedules
        if datetime.combine(s.date, s.end_time) < now
    ]

def get_future_schedules(volunteer_id):
    gmt_tz = pytz.timezone("Europe/Prague")
    now = datetime.now(gmt_tz)
    schedules = get_volunteer_schedules(volunteer_id)
    return [
        s for s in schedules
        if datetime.combine(s.date, s.start_time) > now
    ]

def cancel_volunteer_schedule(schedule_id, volunteer_id):
    schedule = WalkSchedule.query.get(schedule_id)
    if schedule and schedule.volunteer_id == volunteer_id and (schedule.state == ScheduleState.RESERVED.value or schedule.state == ScheduleState.CONFIRMED.value):
        schedule.state = ScheduleState.FREE.value
        schedule.volunteer_id = None
        db.session.commit()
        return True
    return False