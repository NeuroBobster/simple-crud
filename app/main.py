from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.responses import PlainTextResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import IntegrityError
from typing import List

import app.db as db
from app.db import SessionLocal
import app.schemas as schemas


app = FastAPI()


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=422)


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/user", response_model = List[schemas.User])
def read_user_list(session: SessionLocal = Depends(get_session)):
    with session:
        user_list = session.query(db.User).all()
    return user_list


@app.post("/user", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, session: SessionLocal = Depends(get_session)):
    with session:
        user_db = db.User(name=user.name, email=user.email)
        session.add(user_db)
        try:
            session.commit()
        except IntegrityError as e:
            raise HTTPException(status_code=409, detail=f"User creation failed with the following error:\n{e}")
        session.refresh(user_db)
    return user_db


@app.get("/user/{id}")
def read_user(id: int, session: SessionLocal = Depends(get_session)):
    with session:
        user_db = session.query(db.User).get(id)
    
    if not user_db:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")

    return user_db


@app.put("/user/{id}")
def update_user(id: int, user: schemas.UserUpdate, session: SessionLocal = Depends(get_session)):
    with session:
        user_db = session.query(db.User).get(id)
        if user_db:
            if user.name:
                user_db.name = user.name
            if user.email:
                user_db.email = user.email
            session.commit()
        else:
            raise HTTPException(status_code=404, detail=f"User with id {id} not found")
    return user_db


@app.delete("/user/{id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_user(id: int, session: SessionLocal = Depends(get_session)):
    with session:
        user_db = session.query(db.User).get(id)
        if user_db:
            session.delete(user_db)
            session.commit()
        else:
            raise HTTPException(status_code=404, detail=f"User with id {id} not found")
    return None

