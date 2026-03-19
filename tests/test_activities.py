"""Tests for activities endpoints using AAA (Arrange-Act-Assert).

These tests use the in-memory `activities` structure from `src.app`.
"""
import urllib.parse


def test_root_redirect(client):
    # Arrange: client fixture
    # Act
    response = client.get("/", allow_redirects=False)
    # Assert
    assert response.status_code in (307, 308)
    assert response.headers.get("location") == "/static/index.html"


def test_get_all_activities(client):
    # Arrange: client
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "description" in data["Chess Club"]


def test_signup_success(client):
    # Arrange
    activity = urllib.parse.quote("Chess Club", safe="")
    email = "newstudent@example.com"
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]


def test_signup_duplicate(client):
    # Arrange
    activity = urllib.parse.quote("Chess Club", safe="")
    existing = "michael@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": existing})
    # Assert
    assert response.status_code == 400


def test_signup_activity_not_found(client):
    # Arrange
    activity = urllib.parse.quote("NoSuchActivity", safe="")
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": "x@y.com"})
    # Assert
    assert response.status_code == 404


def test_remove_participant(client):
    # Arrange: sign up a temporary participant so test is self-contained
    activity = urllib.parse.quote("Chess Club", safe="")
    email = "temp_remove@example.com"
    signup_resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert signup_resp.status_code == 200

    # Act: remove the participant
    resp = client.delete(f"/activities/{activity}/participants", params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert "Unregistered" in resp.json()["message"]
