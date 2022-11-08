from fastapi.testclient import TestClient

from main import app
from utils.random import create_random_key

client = TestClient(app)

test_user = {
             "email": f"{create_random_key()}@test.com",
             "password": "t3sTpasSw0rD"
             }

# Signup
def test_create_user():
    response = client.post("/signup", json=test_user)
    assert response.status_code == 201
    assert response.json()['detail'] == 'User created successfully'

def test_existing_user():
    response = client.post("/signup", json=test_user)
    assert response.status_code == 400
    assert response.json()['detail'] == 'User already exist'


# Login
def test_login_with_wrong_user():
    payload_bad_user = {
        "username":  (None, "wrong_email@failingtest.com"),
        "password": (None, test_user["password"])
    }
    response = client.post("/login", data=payload_bad_user)
    assert response.status_code == 400
    assert response.json()['detail'] == 'Incorrect email or password'

def test_login_with_wrong_password():
    payload_bad_password = {
        "username":  (None, test_user["email"]),
        "password": (None, "wrong_password")
    }
    response = client.post("/login", data=payload_bad_password)
    assert response.status_code == 400
    assert response.json()['detail'] == 'Incorrect email or password'

def test_login_with_correct_credentials():
    payload = {
        "username":  (None, test_user["email"]),
        "password": (None, test_user["password"])
    }
    response = client.post("/login", data=payload)
    assert response.status_code == 200
    assert 'access_token' in response.json()
