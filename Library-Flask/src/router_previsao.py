from repositorio_previsao import Previsao

def router(app):
    @app.route('/previsao', methods=['GET'])
    def get_previsao():
        return Previsao.get()