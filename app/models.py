from datetime import datetime
import uuid

from app import db
from schemas import RepairRequestStatus


class RepairRequest(db.Model):
    __tablename__ = 'repair_requests'

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    request_date = db.Column(db.DateTime, default=datetime.utcnow)
    device_type = db.Column(db.String(50), nullable=False)
    device_model = db.Column(db.String(50), nullable=False)
    issue_description = db.Column(db.Text, nullable=False)
    client_name = db.Column(db.String(100), nullable=False)
    client_phone = db.Column(db.String(20), nullable=False)
    status = db.Column(db.Enum(RepairRequestStatus), default=RepairRequestStatus.NEW, nullable=False)

    def __repr__(self):
        return f'<RepairRequest {self.id}>'
