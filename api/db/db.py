import time
from typing import Optional

import MySQLdb
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from api import config, log

DATABASE_USERNAME = config.DATABASE_USERNAME
DATABASE_PASSWORD = config.DATABASE_PASSWORD
DATABASE_HOST = config.DATABASE_HOST
DATABASE_PORT = config.DATABASE_PORT
DATABASE_NAME = config.DATABASE_NAME

SQLALCHEMY_DATABASE_URI = (f"mysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}"
                           f"@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}")

class DatabaseInstance:
    def __init__(self):
        self.Base = declarative_base()
        self.db = SQLAlchemy(model_class=self.Base)
        self.engine = create_engine(SQLALCHEMY_DATABASE_URI)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.db.metadata.reflect(self.engine)

    def get_session(self):
        session = self.SessionLocal()
        try:
            return session
        finally:
            session.close()

    def init_app(self, app):
        return self.db.init_app(app)

def wait_for_connection_and_create_instance(wait_time: int, attempts: int) -> Optional[DatabaseInstance]:
    def connect():
        return MySQLdb.connect(
            host=DATABASE_HOST, user=DATABASE_USERNAME, password=DATABASE_PASSWORD,
            port=DATABASE_PORT, database=DATABASE_NAME, connect_timeout=20)

    while attempts != 0:
        try:
            with connect() as conn:
                if not conn:
                    continue

                with conn.cursor() as c:
                    if c.execute('select 1;'):
                        return DatabaseInstance()
        except MySQLdb.OperationalError as e:
            log.exception(e)

        time.sleep(wait_time)
        attempts -= 1
