from datetime import timedelta

from __init__ import db
from models.walk_schedule import WalkSchedule
from models.enums.schedule_state import ScheduleState


#READ ONE
def get_schedule(schedule_id):
    return WalkSchedule.query.get(schedule_id)

#READ FOR ONE ANIMAL
def get_animal_schedules(animal_id):
    return WalkSchedule.query.filter_by(animal_id=animal_id).order_by(WalkSchedule.start_time).all()

#READ SCHEDULES WITCH STATE FREE OR RESERVED FOR ONE ANIMAL
def get_incoming_animal_schedules(animal_id):
    return WalkSchedule.query.filter(
        WalkSchedule.animal_id == animal_id,
        WalkSchedule.state.in_([ScheduleState.FREE.value, ScheduleState.RESERVED.value])
    ).order_by(WalkSchedule.start_time).all()

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
    for count in range(data.get('count')):
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