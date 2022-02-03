from fastapi import FastAPI
from typing import Optional

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/users/{user_id}")
def read_user(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
