import uuid
from datetime import datetime
from ..extensions import db

def uuid_str():
    return str(uuid.uuid4())

class PredictionResult(db.Model):
    __tablename__ = "prediction_results"

    id = db.Column(db.String(36), primary_key=True, default=uuid_str)
    response_id = db.Column(db.String(36), db.ForeignKey("questionnaire_responses.id"), nullable=False)

    model_version = db.Column(db.String(50), nullable=False)
    predicted_label = db.Column(db.String(50), nullable=False)
    proba_json = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
