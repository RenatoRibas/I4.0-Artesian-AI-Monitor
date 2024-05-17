from sqlalchemy import Column, Float, Integer, DateTime, func, String
from flask import jsonify
import db
    
class Motor(db.Base):
    __tablename__ = 'motor'

    id_motor = Column(Integer, primary_key=True)
    tag = Column(String)
    descricao = Column(String)
    frequencia = Column(Float)
    corrente = Column(Float)
    tensao = Column(Float)
    potencia = Column(Float)
    timestamp = Column(DateTime, server_default=func.now())

    def builder(self):
        return {
            'id_motor': self.id_log_motor,
            'tag': self.tag,
            'descricao': self.descricao,
            'frequencia': self.frequencia,
            'corrente': self.corrente,
            'tensao': self.tensao,
            'potencia': self.potencia,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def insert():
        session = db.Session()

        data = session.query(Motor).order_by(Motor.timestamp.desc()).limit(10).all()

        if (len(data) > 0):
            return

        registro = Motor(
            id_motor=1,
            tag='Bomba Poço 1',
            descricao='Bomba Poço 1',
            frequencia=60, 
            corrente=20,
            tensao=380,
            potencia=3.3,
        )

        session.add(registro)

        registro = Motor(
            id_motor=2,
            tag='Bomba Poço 2',
            descricao='Bomba Poço 2',
            frequencia=60, 
            corrente=20,
            tensao=380,
            potencia=3.3,
        )

        session.add(registro)

        registro = Motor(
            id_motor=3,
            tag='Bomba Poço 3',
            descricao='Bomba Poço 3',
            frequencia=60, 
            corrente=20,
            tensao=380,
            potencia=3.3,
        )

        session.add(registro)

        session.commit()
        session.close()

    def get():
        session = db.Session()

        data = session.query(Motor).order_by(Motor.timestamp.desc()).limit(10).all()
        serialized_data = [row.builder() for row in data]
        session.close()

        response = jsonify({'content': serialized_data})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response