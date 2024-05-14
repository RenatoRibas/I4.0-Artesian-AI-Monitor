from flask import Flask, jsonify
from sqlalchemy import create_engine, Column, Float, Integer, DateTime, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)


engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/DW_Server')
Session = sessionmaker(bind=engine)
Base = declarative_base()

class PrevisaoM3h(Base):
    __tablename__ = 'previsaom3h'

    id_previsao = Column(Integer, primary_key=True)
    previsaoregistrada = Column(Float)
    offsettolerancia = Column(Float)
    timestamp = Column(DateTime, server_default=func.now())

    def to_dict(self):
        return {'id_previsao': self.id_previsao,
                'previsaoregistrada': self.previsaoregistrada,
                'offsettolerancia': self.offsettolerancia,
                'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}

@app.route('/previsaom3h/', methods=['GET'])
def get_previsaom3h():
    session = Session()
    data = session.query(PrevisaoM3h).all()
    serialized_data = [row.to_dict() for row in data]
    session.close()
    return jsonify({'previsaom3h': serialized_data})


if __name__ == '__main__':
    app.run(debug=True)
