from app import schemas
from .database import client, session
import pytest

def test_create_user(client):
    res = client.post("/users", json={"email":"santiago@gmail.com","password":"12345678"})
    print(res.json()
          )
    #new_user = schemas.UserOut(**res.json())
    assert res.status_code == 201
    assert res.json().get("email") == "santiago@gmail.com"

@pytest.fixture
def test_user(client):
    user_data = {"email": "aaa@gmail.com",
                 "password": "12345678"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data["password"]
    return new_user


def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user['email'],"password": test_user['password']})
    assert res.status_code == 200
    
@pytest.mark.parametrize("email, password, status_code", [
    ("aadad@gmail.com", "afsdfsfs", 403),
    ("santiago@gmail.com", "12345678", 403),
    (None,"defegesg",403)
])
#def test_incorrect_login(test_user, client):
def test_incorrect_login(test_user, client, email, password, status_code):
    #res = client.post("/login", data={"username": test_user['email'],"password": 'wrongpassword'})
    res = client.post("/login", data={"username": email,"password": password})
    
    assert res.status_code == status_code
    #assert res.json().get('detail') == 'invalid credentials'
    