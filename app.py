from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource 
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres.stuxibzwndpeupvqoknt:TTlS2CZFFNO2xBgm@aws-0-sa-east-1.pooler.supabase.com:5432/postgres'
app.config['JWT_SECRET_KEY'] = 'wwPmrHIXbOwM1VOht53eFk1EH48vwAc1'  
jwt = JWTManager(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


class AuthResource(Resource):
    def post(self):
        data = request.get_json()
        if not data or 'username' not in data or 'password' not in data:
            return make_response(jsonify({'error': 'Informe todos os campos'}), 400)

        username = data['username']
        password = data['password']
        
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            access_token = create_access_token(identity=user.id,additional_claims={'username': user.username, 'id': user.id})
            return make_response(jsonify({'access_token': access_token, 'message': 'Autenticado com sucesso!'}), 200)
        else:
            return make_response(jsonify({'error': 'Usuário ou senha inválidos'}), 401)

api.add_resource(AuthResource, '/auth')

class UserResource(Resource):
    def post(self):
        data = request.get_json()

        print('user ->', data)
        if not data or 'username' not in data or 'password' not in data:
            return make_response(jsonify({'error': 'Informe todos os campos'}), 400) 


        username = data['username']
        password = data['password']
        
        if User.query.filter_by(username=username).first():
            return make_response(jsonify({'error': 'Usuário já existente'}), 400)

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        return make_response(jsonify({'message': 'Usuário criado com sucesso!'}), 201)

api.add_resource(UserResource, '/user')

if __name__ == '__main__':
    app.run(debug=True)