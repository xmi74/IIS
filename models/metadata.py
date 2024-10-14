from __init__ import db

# Metadata table for overcoming duplicate seeding
class Metadata(db.Model):
    __tablename__ = 'metadata'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.String(50), nullable=True)
