from models.examination import Examination, Vaccination, PreventiveCheckUp
from __init__ import db

# CREATE
def create_examination(data):
    if data['type'] == 'vaccination':
        new_examination = Vaccination(
            date=data['date'],
            description=data['description'],
            vet_id=data['vet_id'],
            animal_id=data['animal_id'],
            vaccination_type=data['vaccination_type']
        )
    elif data['type'] == 'preventive_checkup':
        new_examination = PreventiveCheckUp(
            date=data['date'],
            description=data['description'],
            vet_id=data['vet_id'],
            animal_id=data['animal_id']
        )
    else:
        new_examination = Examination(
            date=data['date'],
            description=data['description'],
            vet_id=data['vet_id'],
            animal_id=data['animal_id']
        )

    db.session.add(new_examination)
    db.session.commit()
    return new_examination

# GET ALL
def get_examinations():
    return Examination.query.all()

# GET ONE
def get_examination(examination_id):
    return Examination.query.get_or_404(examination_id)

# GET ALL BY VET ID
def get_examinations_by_vet(vet_id):
    return Examination.query.filter_by(vet_id=vet_id).all()

# GET ALL BY ANIMAL ID
def get_examinations_by_animal(animal_id):
    return Examination.query.filter_by(animal_id=animal_id).all()

# DELETE
def delete_examination(examination_id):
    examination = Examination.query.get_or_404(examination_id)

    db.session.delete(examination)
    db.session.commit()
    return examination
