from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session


db_connection = 'postgresql+psycopg2://postgres:postgres@localhost:5432/alembic'
engine = create_engine(db_connection)

meta = MetaData()
meta.reflect(bind=engine)

db_session = Session(bind=engine)
Base = declarative_base()
