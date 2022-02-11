import os
from app.main import app, get_session
from app.db import Base
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


client = TestClient(app)
os.remove('test.db')
SQLALCHEMY_DATABASE_URL = "sqlite:///test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_session():
    try:
        session = TestingSessionLocal()
        yield session
    finally:
        session.close()


app.dependency_overrides[get_session] = override_get_session


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_get_all_users_when_none():
    response = client.get("/user")
    assert response.status_code == 200
    assert response.json() == []

def test_add_user():
    response = client.post("/user", json={"name": "john smith", "email": "john@gmail.com"})
    assert response.status_code == 201
    assert response.json()["id"] == 1


def test_get_all_users_when_some():
    response = client.get("/user")
    assert response.status_code == 200
    assert response.json() == [{"id": 1, "name": "John Smith", "email": "john@gmail.com"}]


def test_add_user_duplicated_username():
    response = client.post("/user", json={"name": "John Smith", "email": "another_john@gmail.com"})
    assert response.status_code == 409
    

def test_add_user_duplicated_email():
    response = client.post("/user", json={"name": "John Bon Jovi", "email": "john@gmail.com"})
    assert response.status_code == 409


def test_add_user_invalid_email():
    response = client.post("/user", json={"name": "Rick", "email": "gibberish"})
    assert response.status_code == 422
    assert 'value is not a valid email address' in response.text
    response = client.post("/user", json={"name": "Rick", "email": 100})
    assert response.status_code == 422
    assert 'value is not a valid email address' in response.text
    

def test_update_user():
    response = client.put("/user/1", json={"name": "Jim Beam"})
    assert response.status_code == 200
    assert response.json()["name"] == "Jim Beam"
    # response = client.get("/user/1")
    assert response.json()["name"] == "Jim Beam"


def test_update_user_invalid_name():
    response = client.put("/user/1", json={"name": "John"})
    assert response.status_code == 422
    assert 'must contain a space' in response.text


def test_update_user_nonexistent():
    response = client.put("/user/100", json={"name": "Michael Jackson"})
    assert response.status_code == 404
    assert 'User with id 100 not found' in response.text


def test_delete_user_nonexistent():
    response = client.delete("/user/100")
    assert response.status_code == 404
    assert 'User with id 100 not found' in response.text


def test_delete_user():
    response = client.delete("/user/1")
    assert response.status_code == 204
