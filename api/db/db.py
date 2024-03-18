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

Base = declarative_base()


class DatabaseInstance:
    # Class attributes
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    db = SQLAlchemy(model_class=Base)
    db.metadata.reflect(engine)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    @staticmethod
    def get_session():
        session = DatabaseInstance.SessionLocal()
        try:
            return DatabaseInstance.SessionLocal()
        finally:
            session.close()

    @staticmethod
    def get_db():
        return DatabaseInstance.db

    @staticmethod
    def get_metadata():
        return DatabaseInstance.db.metadata

    @staticmethod
    def get_table(table_name: str):
        return DatabaseInstance.db.metadata.tables[table_name]

    @staticmethod
    def init_app(app):
        return DatabaseInstance.db.init_app(app)

                with conn.cursor() as c:
                    if c.execute('select 1;'):
                        return DatabaseInstance()
        except MySQLdb.OperationalError as e:
            log.exception(e)

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
