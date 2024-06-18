from app.database.models import RepairRequest


def register_events(db):
    @db.event.listens_for(RepairRequest, 'after_insert')
    @db.event.listens_for(RepairRequest, 'after_update')
    @db.event.listens_for(RepairRequest, 'after_delete')
    def receive_after_change(mapper, connection, target):
        from app import socketio
        socketio.emit('update', {'message': 'заявки обновленны, перезагрузка страницы через 5 секунд...'})
