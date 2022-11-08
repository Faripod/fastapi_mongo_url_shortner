import json

def test_create_user(client):
    data = {"username":"testuser","email":"testuser@nofoobar.com","password":"testing"}
    response = client.post("/users/",json.dumps(data))
    assert response.status_code == 200 
    assert response.json()["email"] == "testuser@nofoobar.com"
    assert response.json()["is_active"] == True
    
    
    # TODO: test user creation
    # TODO: Test user creation of a user which already exist
    
    # TODO: Test login with fake credential
    # TODO: Test login with previously created credential
