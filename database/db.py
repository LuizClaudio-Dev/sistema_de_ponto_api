import os

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

from .base import Base

load_dotenv(override=True)

SQLALCHEMY_DATABASE_URL = URL.create(
    drivername=os.getenv('database_driver'),
    username=os.getenv('database_user'),
    password=os.getenv('database_password'),
    host=os.getenv('database_host'),
    database=os.getenv('database_name')
)
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/dbname"


class Database:
    def __init__(self):
        self.engine = create_engine(SQLALCHEMY_DATABASE_URL)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine)

    def __enter__(self):
        self.session = self.SessionLocal()
        return self.session

    def create_tables(self):
        Base.metadata.create_all(bind=self.engine)

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()
        self.engine.dispose()
