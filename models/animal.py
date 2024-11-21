from __init__ import db
from datetime import datetime
from sqlalchemy.orm import relationship

from models.enums.animal_species import Species


class Animal(db.Model):
    __tablename__ = 'animals'
    id      = db.Column(db.Integer(), primary_key=True)
    name    = db.Column(db.String(50), nullable=False)
    species = db.Column(db.String(50), nullable=False, default=Species.OTHER.value) #ENUM
    weight  = db.Column(db.Integer(), nullable=True)
    birth_date = db.Column(db.Date(), nullable=True)
    description = db.Column(db.String(500), nullable=True)
    photo   = db.Column(db.String(255), nullable=True) # photo url / default='https://example.com'

    walk_schedules = relationship("WalkSchedule", back_populates="animal")
    examinations = relationship("Examination", back_populates="animal")
    requests = relationship("Request", back_populates="animal")
