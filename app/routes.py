from flask import request, render_template, jsonify
from flask import request, jsonify
from app.models import RepairRequest, RepairRequestStatus
from app.schemas import RepairRequestCreate, RepairRequestResponse, RepairRequestUpdateStatus

def register_routes(app, db):
    @app.route('/')
    def home():
        return render_template('home/home.html')

    @app.route('/repair-requests', methods=['POST'])
    def create_repair_request():
        req_data = request.json
        repair_request_create = RepairRequestCreate(**req_data)
        new_request = RepairRequest(
            device_type=repair_request_create.device_type,
            device_model=repair_request_create.device_model,
            issue_description=repair_request_create.issue_description,
            client_name=repair_request_create.client_name,
            client_phone=repair_request_create.client_phone
        )
        db.session.add(new_request)
        db.session.commit()
        return jsonify(RepairRequestResponse.from_orm(new_request).dict()), 201

    @app.route('/repair-requests/<uuid:request_id>/status', methods=['PATCH'])
    def update_repair_request_status(request_id):
        req_data = request.json
        repair_request_update_status = RepairRequestUpdateStatus(**req_data)
        repair_request = RepairRequest.query.get_or_404(str(request_id))
        repair_request.status = repair_request_update_status.status
        db.session.commit()
        return jsonify(RepairRequestResponse.from_orm(repair_request).dict())