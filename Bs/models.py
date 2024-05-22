# Bs/models.py

from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    price = Column(Float)
    availability = Column(String)
    rating = Column(String)
    image_url = Column(String)
    product_page_url = Column(String)
    upc = Column(String)
    product_type = Column(String)
    price_excl_tax = Column(Float)
    price_incl_tax = Column(Float)
    tax = Column(Float)
    number_of_reviews = Column(Integer)

def get_engine():
    # Replace the connection string with your PostgreSQL credentials
    return create_engine('postgresql+psycopg2://username:password@localhost:5432/mydatabase')

def create_tables():
    engine = get_engine()
    Base.metadata.create_all(engine)
