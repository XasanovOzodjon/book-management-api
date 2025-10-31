from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


class BookBase(BaseModel):
    title: str
    author: str
    genre: str
    year: int
    rating: Decimal


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    year: Optional[int] = None
    rating: Optional[Decimal] = None


class BookResponse(BookBase):
    id: int
    
    class Config:
        from_attributes = True