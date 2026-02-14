import uuid
from datetime import datetime
from ..extensions import db

def uuid_str():
    return str(uuid.uuid4())

class Respondent(db.Model):
    __tablename__ = "respondents"

    id = db.Column(db.String(36), primary_key=True, default=uuid_str)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    consent = db.Column(db.Boolean, default=False, nullable=False)

    # opsional (boleh null demi anonimitas)
    university = db.Column(db.String(150), nullable=True)
    major = db.Column(db.String(150), nullable=True)
    education_level = db.Column(db.String(10), nullable=True)
    batch_year = db.Column(db.Integer, nullable=True)
