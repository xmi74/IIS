from api import api
from models.request import Request
from __init__ import db

# READ ALL
def get_requests():
    return Request.query.all()

# READ ONE
def get_request(request_id):
    return Request.query.get_or_404(request_id)

# FORM?
def create_request():
    pass

# EDIT
def edit_request(request_id, data):
    request = Request.query.get_or_404(request_id)

    request.description = data.get('description', request.description)
    request.caretaker_id = data.get('caretaker_id', request.caretaker_id)
    request.animal_id = data.get('animal_id', request.animal_id)
    request.vet_id = data.get('vet_id', request.vet_id)
    request.confirmed = data.get('confirmed', request.confirmed)

    db.session.commit()

# EDIT CONFIRMED ONLY
def edit_request_confirmed(request_id, new_status):
    request = Request.query.get_or_404(request_id)
    request.confirmed = new_status

    db.session.commit()

# FILTERING
def filter_request(filters):
    query = Request.query

    if 'confirmed' in filters and filters['confirmed']:
        if filters['confirmed'] == 'true':
            query = query.filter[Request.confirmed.is_(True)]
        elif filters['confirmed'] == 'false':
            query = query.filter(Request.confirmed.is_(False))

    return query.all()

# FILTER ONLY REQUESTS BELONGING TO GIVEN VET
def get_requests_by_vet(vet_id, confirmed_filter=None):
    query = Request.query.filter_by(vet_id=vet_id)

    if confirmed_filter is not None:
        query = query.filter(Request.confirmed == confirmed_filter)

    return query.all()

