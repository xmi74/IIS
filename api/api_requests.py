from datetime import datetime

from flask import request

from api import api
import pytz
from models.request import Request
from __init__ import db

# READ ALL
def get_requests():
    return Request.query.all()

# READ ONE
def get_request(request_id):
    return Request.query.get_or_404(request_id)

# FORM?
def create_request(data):
    gmt_tz = pytz.timezone("GMT")
    request = Request(
        vet_id=data.get('vet_id'),
        title=data.get('title'),
        description=data.get('description'),
        created_at=datetime.now(gmt_tz),
        animal_id=data.get('animal_id'),
        caretaker_id=data.get('caretaker_id'),
    )

    try:
        db.session.add(request)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return request


#DELETE
def delete_request(request_id):
    request = get_request(request_id)
    db.session.delete(request)
    db.session.commit()

# EDIT
def edit_request(request_id, data):
    request = Request.query.get_or_404(request_id)

    request.title = data.get("title", request.title)
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

    if 'confirmed' in filters and filters['confirmed'] is not None:
        query = query.filter(Request.confirmed.is_(False))
    if 'animal_id' in filters and filters['animal_id']:
        query = query.filter(Request.animal_id == filters['animal_id'])

    return query.all()

# FILTER ONLY REQUESTS BELONGING TO GIVEN VET
def get_requests_by_vet(vet_id, confirmed_filter=None):
    query = Request.query.filter_by(vet_id=vet_id)

    if confirmed_filter is not None:
        query = query.filter(Request.confirmed == confirmed_filter)

    return query.all()

