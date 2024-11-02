import pymysql
from google.cloud.sql.connector import Connector
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from constants import (
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
    BYPASS_ENDPOINTS,
)


# initialize Connector object
connector = Connector()


# function to return the database connection
def getconn() -> pymysql.connections.Connection:
    conn: pymysql.connections.Connection = connector.connect(
        "uav-as-a-service:us-central1:myinstance", "pymysql", user=DB_USER, password=DB_PASSWORD, db=DB_NAME
    )
    return conn


class SessionManager:
    engine = create_engine(
        "mysql+pymysql://",
        creator=getconn,
    )
    session_class = sessionmaker(bind=engine, autoflush=False)
    ThreadSession = scoped_session(session_class)

    def process_resource(self, req, resp, resource, params):
        if req.method == "OPTIONS" or req.path in BYPASS_ENDPOINTS:
            return
        req.context.instance.add_session(SessionManager.ThreadSession())

    def process_response(self, req, resp, resource, req_succeeded):
        if req.context.instance.db_session is not None:
            if not req_succeeded:
                req.context.instance.db_session.rollback()
            req.context.instance.db_session.close()
