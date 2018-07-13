from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from faq_migrations.settings import config


db_connection = config.database_url
engine = create_engine(db_connection)

meta = MetaData()
meta.reflect(bind=engine)

db_session = Session(bind=engine)
Base = declarative_base()
