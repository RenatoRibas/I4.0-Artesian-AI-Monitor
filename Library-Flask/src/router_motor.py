from repository_motor import Motor

def router(app):
    @app.route('/motor', methods=['GET'])
    def get_motor():
        return Motor.get()
    
    @app.route('/motor', methods=['POST'])
    def save_motor():
        return Motor.save()
    
    @app.route('/motor', methods=['DELETE'])
    def delete_motor():
        return Motor.delete()