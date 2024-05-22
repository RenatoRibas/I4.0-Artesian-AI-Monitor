from repository_log_motor import LogMotor

def router(app):
    @app.route('/log-motor', methods=['GET'])
    def get_log_motor():
        return LogMotor.get()