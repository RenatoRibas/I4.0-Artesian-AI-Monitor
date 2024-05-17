from sqlalchemy import Column, Float, Integer, DateTime, func, Boolean
from flask import jsonify
from repositorio_vazao import Vazao
import db
import random
    
class LogMotor(db.Base):
    __tablename__ = 'log_motor'

    id_log_motor = Column(Integer, primary_key=True)
    id_motor = Column(Integer)
    status = Column(Boolean)
    frequencia = Column(Float)
    corrente = Column(Float)
    tensao_entrada = Column(Float)
    timestamp = Column(DateTime, server_default=func.now())

    def builder(self):
        return {
            'id_log_motor': self.id_log_motor,
            'id_motor': self.id_motor,
            'status': self.status,
            'frequencia': self.frequencia,
            'corrente': self.corrente,
            'tensao_entrada': self.tensao_entrada,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def insert(counter):
        session = db.Session()

        id_motor = random.uniform(1, 3)
        frequencia = random.uniform(58, 62)
        corrente = random.uniform(15, 20)
        tensao_entrada = random.uniform(370, 400)

        registro = LogMotor(
            id_motor=id_motor,
            status=True,
            frequencia=frequencia, 
            corrente=corrente,
            tensao_entrada=tensao_entrada,
        )

        session.add(registro)
        session.commit()

        Vazao.insert(registro.id_log_motor, counter)

        session.close()

    def get():
        session = db.Session()

        data = session.query(LogMotor).order_by(LogMotor.timestamp.desc()).limit(10).all()
        serialized_data = [row.builder() for row in data]
        session.close()

        response = jsonify({'content': serialized_data})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response