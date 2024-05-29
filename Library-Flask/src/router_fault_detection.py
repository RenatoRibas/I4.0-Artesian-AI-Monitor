from flask import request
from flask_jwt_extended import jwt_required
from repository_fault_detection import FaultDetection

def router(app, jwt):
    @app.route('/fault-detection', methods=['GET'])
    @jwt_required()
    def get_fault_detection():
        return FaultDetection.get(request.args)