from datetime import datetime
import uuid

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_manager

from app import db, login_manager

from .schemas import RepairRequestStatus


class RepairWorker(UserMixin, db.Model):
    __tablename__ = 'repair_workers'
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    repair_requests = db.relationship('RepairRequest', back_populates='current_master')

    def __repr__(self):
        return f'<RepairWorker {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return RepairWorker.query.get(user_id)


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
    current_master_id = db.Column(db.String, db.ForeignKey('repair_workers.id'), nullable=True)
    master_comment = db.Column(db.Text, nullable=True)

    current_master = db.relationship('RepairWorker', back_populates='repair_requests')

    def __repr__(self):
        return f'<RepairRequest {self.id}>'

