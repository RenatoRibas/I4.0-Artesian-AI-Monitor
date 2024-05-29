from flask import request, jsonify
from flask_jwt_extended import create_access_token

USERS = {
    "admin": "admin"
}

def router(app, jwt):
    @app.route('/auth', methods=['POST'])
    def auth():
        if not request.is_json:
            return jsonify({"mensagem": "Solicitação deve ser JSON"}), 400

        username = request.json.get('username')
        password = request.json.get('password')

        if not username or not password:
            return jsonify({"mensagem": "Credenciais inválidas"}), 400

        if username not in USERS or USERS[username] != password:
            return jsonify({"mensagem": "Credenciais inválidas"}), 401

        token = create_access_token(identity=username)

        return jsonify({
            "id": 1,
            "name": "Administrador",
            "role": "admin",
            "email": "admin@artesian.com.br",
            "token": token
        }), 200