from __init__ import db
from models.walk_schedule import WalkSchedule


#READ ONE
def get_schedule(schedule_id):
    return WalkSchedule.query.get(schedule_id)

#READ FOR ONE ANIMAL
def get_animal_schedules(animal_id):
    return WalkSchedule.query.filter_by(animal_id=animal_id).order_by(WalkSchedule.start_time).all()

#DELETE
def delete_schedule(schedule_id):
    schedule = WalkSchedule.query.get(schedule_id)
    db.session.delete(schedule)
    db.session.commit()
    return schedule

#CREATE
#TODO
def create_schedule(schedule):
    raise NotImplemented

#EDIT
def edit_schedule(id, new_schedule):
    schedule = WalkSchedule.query.get_or_404(id)
    schedule.start_time = new_schedule.get('start_time')
    schedule.end_time = new_schedule.get('end_time')
    schedule.state = new_schedule.get('state')

    try:
        db.session.commit()
    except Exception as e:
        print(f"Error commiting to database: {str(e)}")
        raise
    return schedule