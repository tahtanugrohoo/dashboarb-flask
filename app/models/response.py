import uuid
from datetime import datetime
from ..extensions import db

def uuid_str():
    return str(uuid.uuid4())

class QuestionnaireResponse(db.Model):
    __tablename__ = "questionnaire_responses"

    id = db.Column(db.String(36), primary_key=True, default=uuid_str)
    respondent_id = db.Column(db.String(36), db.ForeignKey("respondents.id"), nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Simpan jawaban dulu bentuk JSON (biar fleksibel)
    answers_json = db.Column(db.JSON, nullable=False)

    # versi mapping fitur (untuk skripsi)
    data_version = db.Column(db.String(20), default="v1", nullable=False)

    respondent = db.relationship("Respondent", backref=db.backref("responses", lazy=True))
