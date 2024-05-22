from sqlalchemy import Column, Float, Integer, DateTime, func
from flask import jsonify
import db
import random

class Flow(db.Base):
    __tablename__ = 'vazao'

    id_vazao = Column(Integer, primary_key=True)
    id_log_motor = Column(Integer)
    vazao_registrada = Column(Float)
    timestamp = Column(DateTime, server_default=func.now())

    def builder(self):
        return {
            'id_vazao': self.id_vazao,
            'id_log_motor': self.id_log_motor,
            'vazao_registrada': self.vazao_registrada,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def insert(id_log_motor, counter, fault_counter):
        session = db.Session()

        flow = random.uniform(24.36, 25.47)

        if counter == fault_counter:
            flow = random.uniform(19.36, 22.47)

        register = Flow(
            id_log_motor=id_log_motor,
            vazao_registrada=flow,
        )

        session.add(register)
        session.commit()
        session.close()

    def get():
        session = db.Session()

        data = session.query(Flow).order_by(Flow.timestamp.desc()).limit(10).all()
        serialized_data = [row.builder() for row in data]
        session.close()

        response = jsonify({'content': serialized_data})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response