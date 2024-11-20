from sqlalchemy.orm import relationship
from flask_login import UserMixin
from __init__ import db, bcrypt

# Single inheritance table => all Admin/User/Caretaker/Vet records are stored in users table
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id         = db.Column(db.Integer(), primary_key=True)
    login      = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name  = db.Column(db.String(50), nullable=False)
    email      = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    role       = db.Column(db.String(20), nullable=False) # Enum
    verified   = db.Column(db.Boolean(), default=False)  # Specified for volunteer


    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': role      # Defines type of subclass
    }

    # Getter for password
    @property
    def password(self):
        return self.password

    # Setter for password - creating hashed password
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    # Function for checking passwords when logging in
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

class Admin(User):
    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }

class Caretaker(User):
    walk_schedules = relationship("WalkSchedule", back_populates="caretaker", foreign_keys="[WalkSchedule.caretaker_id]")
    requests = relationship("Request", back_populates="caretaker", foreign_keys="[Request.caretaker_id]")  # Použitie reťazca pre vzťah

    __mapper_args__ = {
        'polymorphic_identity': 'caretaker'
    }

class Vet(User):
    # 1:N Examination, Overlaps = silencing same foreign key warning
    examinations = relationship("Examination", back_populates="vet", overlaps="vaccinations") 
    # 1:N Vaccination, Overlaps = silencing same foreign key warning
    vaccinations = relationship("Vaccination", back_populates="vet", overlaps="examinations")
    requests = relationship("Request", back_populates="vet", foreign_keys="[Request.vet_id]")

    __mapper_args__ = {
        'polymorphic_identity': 'vet'
    }

class Volunteer(User):
    walk_schedules = relationship("WalkSchedule", back_populates="volunteer", foreign_keys="[WalkSchedule.volunteer_id]") # 1:N WalkSchedule

    __mapper_args__ = {
        'polymorphic_identity': 'volunteer'
    }

