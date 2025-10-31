from sqlalchemy import Column, Integer, String, Numeric
from app.db import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    author = Column(String, index=True, nullable=False)
    genre = Column(String, index=True, nullable=False)
    year = Column(Integer, nullable=False)
    rating = Column(Numeric(3,2), nullable=False)