from flask import abort
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        abort(404)


class UserModelView(ModelView):
    # Колонки, которые будут отображены
    column_list = ('id', 'username', 'email', 'password_hash', 'is_admin', 'is_manager', 'is_repairman',)
    # Колонки, доступные для редактирования
    form_columns = ['id', 'username', 'email', 'password_hash', 'is_admin', 'is_manager', 'is_repairman']

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        abort(404)


class RequestModelView(ModelView):
    column_list = (
                    'id', 'request_date', 'device_type', 'device_model', 'issue_description', 'client_name',
                    'client_phone', 'status', 'current_master_id', 'master_comment', 'is_active', 'complete_at'
                    )
    form_columns = ['request_date', 'device_type', 'device_model', 'issue_description', 'client_name', 'client_phone',
                    'status', 'current_master_id', 'master_comment', 'is_active', 'complete_at'
                    ]


def create_admin(app):
    admin = Admin(app, index_view=MyAdminIndexView(), template_mode='bootstrap4')
    from app.database.models import db, User, RepairRequest
    admin.add_view(UserModelView(User, db.session))
    admin.add_view(RequestModelView(RepairRequest, db.session))
    return admin
