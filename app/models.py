from datetime import datetime
import uuid

from app import db
from .schemas import RepairRequestStatus


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
    current_master_id = db.Column(db.String, db.ForeignKey('repair_workers.id', name='fk_repair_requests_current_master_id'), nullable=True)
    master_comment = db.Column(db.Text, nullable=True)

    current_master = db.relationship('RepairWorker', back_populates='repair_requests')

    def __repr__(self):
        return f'<RepairRequest {self.id}>'


class RepairWorker(db.Model):
    __tablename__ = 'repair_workers'

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    repair_requests = db.relationship('RepairRequest', back_populates='current_master')

    def __repr__(self):
        return f'<RepairWorker {self.id}>'
