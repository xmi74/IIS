from __init__ import db
from datetime import datetime
from sqlalchemy.orm import relationship

class Animal(db.Model):
    __tablename__ = 'animals'
    id      = db.Column(db.Integer(), primary_key=True)
    name    = db.Column(db.String(50), nullable=False)
    species = db.Column(db.String(50), nullable=False)
    age     = db.Column(db.Integer(), nullable=False)
    weight  = db.Column(db.Integer(), nullable=False)
    birth_date = db.Column(db.DateTime(), nullable=True)
    photo   = db.Column(db.String(255), nullable=True) # photo url / default='https://example.com'

    walk_schedules = relationship("WalkSchedule", back_populates="animal")
    examinations = relationship("Examination", back_populates="animal")

    