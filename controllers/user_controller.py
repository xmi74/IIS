from __init__ import db
from models.user import User, Admin, Caretaker, Vet, Volunteer

class UserController:
    def getVolunteers(self, validated=None):
        users = Volunteer.query.all()
        result = [
            {
                "id": user.id,
                "login": user.login,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
                "verified": user.verified,
            } for user in users
        ]
        return result

    def valideteVolunteer(self, user_id, validate=False):
        print(validate)
        user = Volunteer.query.filter_by(id=user_id).first()
        user.verified = validate
        db.session.add(user)
        db.session.commit()