from repository_flow import Flow
from flask_jwt_extended import jwt_required

def router(app, jwt):
    @app.route('/flow', methods=['GET'])
    @jwt_required()
    def get_flow():
        return Flow.get()