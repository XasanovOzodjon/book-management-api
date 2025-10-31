from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.core.config import config


DATABASE_URL = URL.create(
    drivername='postgresql+psycopg2',
    host=config.DB_HOST,
    port=config.DB_PORT,
    username=config.DB_USER,
    password=config.DB_PASS,
    database=config.DB_NAME
)

engine = create_engine(url=DATABASE_URL)
Base = declarative_base()
LocalSession = sessionmaker(bind=engine)
def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()