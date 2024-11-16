from flask import jsonify, request
from api import api
from models.animal import Animal
from __init__ import db

# Api functions
# FILTER

# READ ALL (GET)
@api.route('/api/animals', methods=['GET'])
def get_animals():
    animals = Animal.query.all()
    result = [
        {
            "id": animal.id,
            "name": animal.name,
            "species": animal.species,            
            "weight": animal.weight,
            "birth_date": animal.birth_date,
            "photo": animal.photo,
        } for animal in animals
    ]
    return jsonify(result)

# READ ONE (GET)
@api.route('/api/animals/<int:animal_id>', methods=['GET'])
def get_animal():
    animal = Animal.query.get_or_404(animal_id)
    result = [
        {
            "id": animal.id,
            "name": animal.name,
            "species": animal.species,            
            "weight": animal.weight,
            "birth_date": animal.birth_date,
            "photo": animal.photo,
        }
    ]
    return jsonify(result)

# CREATE (POST)
@api.route('/api/animals', methods=['POST'])
def create_animal():
    data = request.get_json()
    new_animal = Animal(name=data['name'], species=data['species'], weight=data['weight'], birth_date=data['birth_date'], photo=data['photo'])

    db.session.add(new_animal)
    db.session.commit()
    return jsonify({"message": "Animal created", "id": new_animal.id })

# EDIT
@api.route('/api/animals/<int:animal_id>', methods=['PUT'])
def edit_animal(animal_id):
    animal = Animal.query.get_or_404(animal_id)
    data = request.get_json()
    animal.name = data.get('name', animal.name)
    animal.species = data.get('species', animal.species)
    animal.weight = data.get('weight', animal.weight)
    animal.birth_date = data.get('birth_date', animal.birth_date)
    animal.photo = data.get('photo', animal.photo)

    db.session.commit()
    return jsonify({"message": "Animal updated", "id": animal.id})

# DELETE
@api.route('/api/animals/<int:animal_id>', methods=['DELETE'])
def delete_animal(animal_id):
    animal = Animal.query.get_or_404(animal_id)
    db.session.delete(animal)

# FILTER
@api.route('/api/animals/search', methods=['GET'])
def filter_animals():
    query = Animal.query
    # Can add more filters
    name = request.args.get('name')
    species = request.args.get('species')
    min_weight = request.args.get('min_weight')
    max_weight = request.args.get('max_weight')

    if name:
        query = query.filter(Animal.name.ilike(f"%{name}%"))
    if species:
        query = query.filter_by(species=species)
    if min_weight:
        query = query.filter(Animal.weight >= int(min_weight))
    if max_weight:
        query = query.filter(Animal.weight <= int(max_weight))

    animals = query.all()
    result = [
        {
            "id": animal.id,
            "name": animal.name,
            "species": animal.species,            
            "weight": animal.weight,
            "birth_date": animal.birth_date,
            "photo": animal.photo,
        } for animal in animals
    ]
    return jsonify(result)
