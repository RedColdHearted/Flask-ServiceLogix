from datetime import datetime, timezone
import uuid

from flask_login import UserMixin

from app import db, login_manager, bcrypt
from app.schemas import RepairRequestStatus


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(100), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=True)
    is_manager = db.Column(db.Boolean, default=False, nullable=True)
    is_repairman = db.Column(db.Boolean, default=False, nullable=True)

    repair_requests = db.relationship('RepairRequest', back_populates='current_master')

    def __str__(self):
        return f'{self.username}'

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    # Method to check password
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class RepairRequest(db.Model):
    __tablename__ = 'repair_requests'

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    request_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc).date())
    device_type = db.Column(db.String(50), nullable=False)
    device_model = db.Column(db.String(50), nullable=False)
    issue_description = db.Column(db.Text, nullable=False)
    client_name = db.Column(db.String(100), nullable=False)
    client_phone = db.Column(db.String(20), nullable=False)
    status = db.Column(db.Enum(RepairRequestStatus), default=RepairRequestStatus.NEW, nullable=False)
    current_master_id = db.Column(db.String(100), db.ForeignKey('users.id'), nullable=True)
    master_comment = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=True)
    complete_at = db.Column(db.DateTime, default=None, nullable=True)

    current_master = db.relationship('User', back_populates='repair_requests')

    def __repr__(self):
        return f'<RepairRequest {self.id}>'


@db.event.listens_for(RepairRequest, 'after_insert')
@db.event.listens_for(RepairRequest, 'after_update')
@db.event.listens_for(RepairRequest, 'after_delete')
def receive_after_change(mapper, connection, target):
    from app import socketio
    socketio.emit('update', {'message': 'заявки обновленны, перезагрузка страницы через 5 секунд...'})