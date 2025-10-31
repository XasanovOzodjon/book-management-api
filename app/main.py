from fastapi import FastAPI
from app.routers.books import router as books
from app.db import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(books)
