def test_register_user(client):
    response = client.post(
        "/api/v1/users/register",
        json={
            "phone_number": "+1987654321",
            "name": "Test User",
            "language_preference": "en"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["phone_number"] == "+1987654321"
    assert data["name"] == "Test User"
    assert data["language_preference"] == "en"
    assert "id" in data

def test_get_user_profile(client):
    # First register a user
    client.post(
        "/api/v1/users/register",
        json={
            "phone_number": "+1122334455",
            "name": "Profile User"
        }
    )
    
    # Then get the profile
    response = client.get("/api/v1/users/+1122334455")
    assert response.status_code == 200
    data = response.json()
    assert data["phone_number"] == "+1122334455"
    assert data["name"] == "Profile User"
    assert data["language_preference"] == "hi"

def test_update_user_preferences(client):
    # First register a user
    client.post(
        "/api/v1/users/register",
        json={
            "phone_number": "+5544332211",
            "name": "Update User"
        }
    )
    
    # Then update preferences
    response = client.put(
        "/api/v1/users/+5544332211/preferences",
        json={
            "language_preference": "bn"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["language_preference"] == "bn"
    assert data["name"] == "Update User" # unchanged
