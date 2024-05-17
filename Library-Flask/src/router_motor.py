from repositorio_motor import Motor

def router(app):
    @app.route('/motor', methods=['GET'])
    def get_motor():
        return Motor.get()