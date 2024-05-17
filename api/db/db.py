import time
from typing import Self, Optional

import MySQLdb
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
# from sqlalchemy.ext.automap import automap_base
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base

from sqlalchemy.orm import sessionmaker

from api import config, log

DATABASE_USERNAME = config.MYSQL_USER
DATABASE_PASSWORD = config.MYSQL_PASSWORD
DATABASE_HOST = config.MYSQL_HOST
DATABASE_PORT = config.MYSQL_PORT
DATABASE_NAME = config.MYSQL_DATABASE

SQLALCHEMY_DATABASE_URI = (f"mysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}"
                           f"@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}")

Base = declarative_base()
# Base = automap_base()


class DatabaseInstance:
    _instance = None

    def __init__(self):
        self.engine = create_engine(SQLALCHEMY_DATABASE_URI)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.db = SQLAlchemy(model_class=Base)
        self.db.metadata.reflect(self.engine)

    def init_app(self, app):
        return self.db.init_app(app)

    def session(self):
        return self.SessionLocal()

    def get_db(self):
        return self.db

    def get_metadata(self):
        return self.db.metadata

    def get_table(self, table_name: str):
        return self.db.metadata.tables[table_name]

    @staticmethod
    def wait_for_connection_and_create_instance(wait_time: int, attempts: int) -> Optional[Self]:
        if DatabaseInstance._instance is not None:
            raise RuntimeError('The global instance already exists')

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
                            instance = DatabaseInstance()
                            DatabaseInstance._instance = instance
                            return instance
            except MySQLdb.OperationalError as e:
                (code, message) = e.args

                if code == 2002: # CR_CONNECTION_ERROR
                    log.info(f'Could not connect to the DB ({message}). Waiting...')
                else:
                    raise

            time.sleep(wait_time)
            attempts -= 1

    @staticmethod
    def get() -> Self:
        return DatabaseInstance._instance
