from databases import Database
from schema import Base
from utils.configuration import Configuration
from sqlalchemy import create_engine

conn_string = Configuration.load('database_connections:postgresql:default')

engine = create_engine(conn_string)

Base.metadata.create_all(engine)