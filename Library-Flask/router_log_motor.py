from repository_log_motor import LogMotor
from flask_jwt_extended import jwt_required

def router(app, jwt):
    @app.route('/log-motor', methods=['GET'])
    @jwt_required()
    def get_log_motor():
        return LogMotor.get()