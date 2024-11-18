from __init__ import db
from datetime import date
from sqlalchemy.orm import relationship
from models.enums.schedule_state import ScheduleState

class WalkSchedule(db.Model):
    __tablename__ = 'walk_schedules'
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.Date(), nullable=False, default=date.today())
    start_time = db.Column(db.Time(), nullable=False)
    end_time = db.Column(db.Time(), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    state = db.Column(db.String(20), nullable=False, default=ScheduleState.FREE.value) # ENUM

    animal_id = db.Column(db.Integer(), db.ForeignKey('animals.id', ondelete="CASCADE"), nullable=False)
    caretaker_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    volunteer_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete="CASCADE"), nullable=True)

    animal = relationship("Animal", back_populates="walk_schedules") # 1:N Animal
    caretaker = relationship("Caretaker", back_populates="walk_schedules", foreign_keys=[caretaker_id]) # 1:N Caretaker
    volunteer = relationship("Volunteer", back_populates="walk_schedules", foreign_keys=[volunteer_id]) # 1:N Volunteer
    