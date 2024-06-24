import os
from logging import getLogger, DEBUG

from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


logger = getLogger(__name__)
logger.setLevel(DEBUG)


POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = int(os.getenv('POSTGRES_PORT'))
SSL_REQUIRE = os.getenv('SSL_REQUIRE', 'True') == 'True'

DB_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'


engine = create_engine(DB_URL)

Session = sessionmaker()
session = Session(bind=engine)


def session_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            session.rollback()
            logger.exception(f"An error occurred during the database query: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred during the database query: {e}.")

    return wrapper
