from repository_flow import Flow

def router(app):
    @app.route('/flow', methods=['GET'])
    def get_flow():
        return Flow.get()