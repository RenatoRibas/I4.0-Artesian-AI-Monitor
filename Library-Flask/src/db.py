from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/DW_Server')
engine = create_engine('postgresql://postgres:admin@localhost:5433/postgres')
Session = sessionmaker(bind=engine)
Base = declarative_base()