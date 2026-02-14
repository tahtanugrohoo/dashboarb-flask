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

    # A. Profil Responden (sesuai kuesioner)
    name_optional = db.Column(db.String(150), nullable=True)   # A1 opsional
    university = db.Column(db.String(150), nullable=True)      # A2
    major = db.Column(db.String(150), nullable=True)           # A3
    semester = db.Column(db.String(10), nullable=True)         # A4
    used_ai = db.Column(db.Boolean, nullable=True)             # A5
