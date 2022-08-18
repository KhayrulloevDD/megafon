from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv


load_dotenv()
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
pg_address = os.getenv("ADDRESS")
pg_port = os.getenv("POSTGRES_PORT")
pg_db = os.getenv("DB")

SQLALCHEMY_DATABASE_URL = f"postgresql://{username}:{password}@{pg_address}:{pg_port}/{pg_db}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, implicit_returning=False
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
