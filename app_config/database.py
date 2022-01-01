from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app_config import config

# follow the documentation on https://fastapi.tiangolo.com/tutorial/sql-databases/ from step: "Create the SQLAlchemy parts"
# postgresql tutorial: https://www.postgresqltutorial.com/postgresql-inner-join/

# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:admin@localhost/FastAPIDB'

SQLALCHEMY_DATABASE_URL = f'postgresql://{config.settings.database_username}:{config.settings.database_password}@{config.settings.database_hostname}/{config.settings.database_name}'

# print("config.Settings.database_username: " + config.Settings.database_username)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency: every time a call to the api is done it will create a session for the db, and after it is done it will close the db session.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()