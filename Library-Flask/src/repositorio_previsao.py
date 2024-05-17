from sqlalchemy import Column, Float, Integer, DateTime, func
from flask import jsonify
import db

class Previsao(db.Base):
    __tablename__ = 'previsao'

    id_previsao = Column(Integer, primary_key=True)
    previsao_registrada = Column(Float)
    offset_tolerancia = Column(Float)
    timestamp = Column(DateTime, server_default=func.now())

    def builder(self):
        return {
            'id_previsao': self.id_previsao,
            'previsao_registrada': self.previsao_registrada,
            'offset_tolerancia': self.offset_tolerancia,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def insert(counter):
        session = db.Session()

        previsao = 0

        if counter == 10:
            previsao = 1

        registro = Previsao(
            previsao_registrada=previsao, 
            offset_tolerancia=24.35
        )

        session.add(registro)
        session.commit()
        session.close()

    def get():
        session = db.Session()

        data = session.query(Previsao).order_by(Previsao.timestamp.desc()).limit(10).all()
        serialized_data = [row.builder() for row in data]
        session.close()

        response = jsonify({'content': serialized_data})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response