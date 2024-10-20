from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQL_DB = "sqlite:///./mydb.db"
engine = create_engine(SQL_DB, connect_args={"check_same_thread": False})

session_local = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()