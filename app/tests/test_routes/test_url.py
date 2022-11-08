from fastapi.testclient import TestClient

from main import app
from utils.random import create_random_key

client = TestClient(app)

test_user = {
        "email": f"{create_random_key()}@test.com",
        "password": "t3sTpasSw0rD"
    }
payload_login = {
        "username":  (None, test_user["email"]),
        "password": (None, test_user["password"])
    }
payload_body = {
    "target_url": f"https://www.google.com?cache_burster={create_random_key()}"
    }
response = client.post("/signup", json=test_user)
response = client.post("/login", payload_login)
fake_bearer_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
bearer_token = response.json()['access_token']
good_headers = {"Authorization": f"Bearer {bearer_token}"}

#  url
def test_url_creation_with_invalid_token():
    headers = {
        "Authorization": f"Bearer {fake_bearer_token}"
    }
    response = client.post("/url", json=payload_body, headers=headers)
    assert response.status_code == 401
    assert response.json()['detail'] == 'Could not validate credentials'


def test_url_creation_with_invalid_url():
    payload = {
        "target_url": "not_a_valid_url"
    }
    response = client.post("/url", json=payload, headers=good_headers)
    assert response.status_code == 400
    assert response.json()['detail'] == 'Not a valid URL'


def test_url_creation():
    response = client.post("/url", json=payload_body, headers=good_headers)
    assert response.status_code == 200
    assert response.json()['msg'] == 'Your URL has been created successfully'

url_key = ""
def test_url_creation_that_already_exists():
    response = client.post("/url", json=payload_body, headers=good_headers)
    assert response.status_code == 200
    assert response.json()['msg'] == 'URL already minified'
    url_key = response.json()['url'].split("/")[-1]

def test_redirect_to_original_url():
    response = client.get(f"/{url_key}")
    assert response.status_code == 200