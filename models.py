from sqlalchemy import Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./dictionary.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Dictionary(Base):
    __tablename__ = "Ibani_dictionary"  # Ensure this matches your table name

    Ibani_word = Column(String, primary_key=True)  # Match the casing used in the database
    Pos = Column(String)
    Meaning = Column(String)
