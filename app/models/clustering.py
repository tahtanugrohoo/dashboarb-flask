import uuid
from datetime import datetime
from ..extensions import db

def uuid_str():
    return str(uuid.uuid4())

class ClusteringResult(db.Model):
    __tablename__ = "clustering_results"

    id = db.Column(db.String(36), primary_key=True, default=uuid_str)
    response_id = db.Column(db.String(36), db.ForeignKey("questionnaire_responses.id"), nullable=False)

    model_version = db.Column(db.String(50), nullable=False)
    cluster_id = db.Column(db.Integer, nullable=False)
    segment_label = db.Column(db.String(50), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
