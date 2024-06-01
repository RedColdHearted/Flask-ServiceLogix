from flask import abort
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        abort(404)


class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        abort(404)


def create_admin(app):
    admin = Admin(app, index_view=MyAdminIndexView())
    from .models import db, RepairWorker, Manager
    admin.add_view(MyModelView(RepairWorker, db.session))
    admin.add_view(MyModelView(Manager, db.session))
    return admin
