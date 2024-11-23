from __init__ import db
from datetime import datetime
from sqlalchemy.orm import relationship

class Request(db.Model):
    __tablename__ = 'requests'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now)
    confirmed = db.Column(db.Boolean(), nullable=False, default=False)

    # Foregin Keys => Request is created for given vet to take care of it
    caretaker_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    animal_id = db.Column(db.Integer(), db.ForeignKey('animals.id', ondelete="CASCADE"), nullable=False)
    vet_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete="CASCADE"), nullable=True)
    
    caretaker = relationship("Caretaker", back_populates="requests", foreign_keys=[caretaker_id])
    animal = relationship("Animal", back_populates="requests")
    vet = relationship("Vet", back_populates="requests", foreign_keys=[vet_id])
    