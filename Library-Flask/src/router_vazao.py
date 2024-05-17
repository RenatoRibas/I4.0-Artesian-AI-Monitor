from repositorio_vazao import Vazao

def router(app):
    @app.route('/vazao', methods=['GET'])
    def get_vazao():
        return Vazao.get()