from __init__ import db
from datetime import datetime
from sqlalchemy.orm import relationship

class Examination(db.Model):
    __tablename__ = 'examinations'
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.DateTime(), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    type = db.Column(db.String(50))

    animal_id = db.Column(db.Integer(), db.ForeignKey('animals.id', ondelete="CASCADE"), nullable=False)
    vet_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)

    # 1:N Animal
    animal = relationship("Animal", back_populates="examinations") 
    # 1:N Vet, Overlaps = silencing same foreign key warning
    vet = relationship("Vet", back_populates="examinations", overlaps="vaccinations") 

    __mapper_args__ = {
        'polymorphic_identity': 'examination',
        'polymorphic_on': type
    }

class Vaccination(Examination):
    __tablename__ = 'vaccinations'
    id = db.Column(db.Integer(), db.ForeignKey('examinations.id'), primary_key=True)
    vaccination_type = db.Column(db.String(50), nullable=True) # Enum for vaccination

    # 1:N Vaccination with Vet, Overlaps = silencing same foreign key warning
    vet = relationship("Vet", back_populates="vaccinations", overlaps="examinations") 

    __mapper_args__ = {
        'polymorphic_identity': 'vaccination'
    }

class PreventiveCheckUp(Examination):
    __tablename__ = 'preventive_checkups'
    id = db.Column(db.Integer(), db.ForeignKey('examinations.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'preventive_checkup'
    }


