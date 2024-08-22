from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./IbaniDictionary.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Dictionary(Base):
    __tablename__ = "dictionary"  # Ensure this matches the table name in your database

    id = Column(Integer, primary_key=True, index=True)
    ibani = Column(String)
    pos = Column(String)
    meaning = Column(String)
