from repository_motor import Motor
from flask_jwt_extended import jwt_required
from flask import request, jsonify
import tools

def router(app, jwt):
    @app.route('/motor', methods=['GET'])
    @jwt_required()
    def get_motor():
        return Motor.get()
    
    @app.route('/motor', methods=['POST'])
    @jwt_required()
    def save_motor():
        return Motor.save(tools.requestFormatter(request)["body"])
    
    @app.route('/motor/<int:id_motor>', methods=['DELETE', 'OPTIONS'])
    @jwt_required()
    def delete_motor(id_motor):
        if request.method == 'OPTIONS':
            response = jsonify({"mensagem": "Permitido"})
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            response.headers.add('Access-Control-Allow-Methods', 'DELETE')
            return response
        elif request.method == 'DELETE':
            return Motor.delete(id_motor)