from fastapi import APIRouter, Depends, HTTPException
from app.db import LocalSession, get_db
from sqlalchemy.orm import Session
from app.models.Book import Book
from app.schemas.book import BookCreate, BookUpdate, BookResponse
from typing import List
import datetime

router = APIRouter(
    prefix="/books",
    tags=["books"],
)


@router.get("/", response_model=List[BookResponse])
def get_all_books(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return books

@router.get("/search")
def search_books(query: str, db: Session = Depends(get_db)):
    books = db.query(Book).filter(
        (Book.title.ilike(f"%{query}%")) |
        (Book.author.ilike(f"%{query}%"))
    ).all()
    return books

@router.get("/filter")
def filter_books(min: int | None, max: int | None, db: Session = Depends(get_db)):
    if min is None:
        min = 0
    if max is None:
        max = 9999
    books = db.query(Book).filter(Book.year.between(min, max)).all()
    return books

@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/", response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    
    if book.year < 0 or book.year > datetime.datetime.now().year:
        raise HTTPException(status_code=400, detail="Yil 0 dan katta va joriy yildan oshmasligi kerak")
    
    if book.rating < 0 or book.rating > 5:
        raise HTTPException(status_code=400, detail="Rayting 0.0 dan 5.0 gacha bolishi kerak")
    
    book = db.query(Book).filter(Book.title == book.title, Book.author == book.author).first()
    if book:
        raise HTTPException(status_code=400, detail="Bu kitob mavjud")
    
    db_book = Book(
        title=book.title,
        author=book.author,
        genre=book.genre,
        year=book.year,
        rating=book.rating
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, updated_book: BookUpdate, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    update_data = updated_book.dict(exclude_unset=True)
    for key, value in update_data.items():
        if key == "title":
            book.title = value
        elif key == "author":
            book.author = value
        elif key == "genre":
            book.genre = value
        elif key == "year":
            if value < 0 or value > datetime.datetime.now().year:
                raise HTTPException(status_code=400, detail="Yil 0 dan katta va joriy yildan oshmasligi kerak")
            book.year = value
        elif key == "rating":
            if value < 0 or value > 5:
                raise HTTPException(status_code=400, detail="Rayting 0.0 dan 5.0 gacha bolishi kerak")
            book.rating = value
    
    db.commit()
    db.refresh(book)
    return book

@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(book)
    db.commit()
    return {"detail": "Book deleted successfully"}