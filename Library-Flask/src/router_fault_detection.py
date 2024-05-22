from flask import request, jsonify
from repository_fault_detection import FaultDetection

def router(app):
    @app.route('/fault-detection', methods=['GET'])
    def get_fault_detection():
        params = {}

        for key in request.args:
            params[key] = request.args.get(key)

        return FaultDetection.get(params)