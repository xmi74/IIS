from re import search

from models.animal import Animal
from __init__ import db


#READ ALL
def get_animals(filters=None):
    if filters is None:
        filters = {}
        
    query = Animal.query

    if 'name' in filters and filters['name'] is not None:
        name = '%{}%'.format(filters['name'])
        query = query.filter(Animal.name.like(name))

    if 'species' in filters and filters['species'] is not None:
        query = query.filter(Animal.species == filters['species'])

    return query.all()

#READ ONE
def get_animal(id):
    return Animal.query.get_or_404(id)

#CREATE
def add_animal(animal):
    new_animal = Animal(
        name=animal.get('name'),
        species= animal.get('species'),
        weight=animal.get('weight'),
        birth_date=animal.get('birth_date'),
        photo=animal.get('photo'),
    )
    db.session.add(new_animal)
    db.session.commit()
    return new_animal

#DELETE
def delete_animal(id):
    animal = Animal.query.get_or_404(id)
    db.session.delete(animal)
    db.session.commit()
    return animal

#EDIT
def edit_animal(id, new_animal):
    animal = Animal.query.get_or_404(id)
    animal.name = new_animal.get('name')
    animal.species = new_animal.get('species')
    animal.weight = new_animal.get('weight')
    animal.birth_date = new_animal.get('birth_date')
    animal.photo = new_animal.get('photo')

    try:
        db.session.commit()
    except Exception as e:
        print(f"Error commiting to database: {str(e)}")
        raise
    return animal

#GET PHOTOS OF LIMITED NUMBER OF ANIMALS
def get_animal_photos(limit=4):
    return Animal.query.filter(Animal.photo.isnot(None)).limit(limit).all()
