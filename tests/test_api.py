from fastapi.testclient import TestClient
from src.app import app
import uuid
import urllib.parse

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Ensure a known activity from the app exists
    assert "Basketball Team" in data


def test_signup_reflects_immediately():
    activity = "Basketball Team"
    email = f"test-{uuid.uuid4().hex}@example.com"

    # Signup
    resp = client.post(f"/activities/{urllib.parse.quote(activity)}/signup", params={"email": email})
    assert resp.status_code == 200, resp.text

    # Immediately fetch activities and confirm participant present
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert email in data[activity]["participants"]


def test_unregister_reflects_immediately():
    activity = "Basketball Team"
    email = f"test-{uuid.uuid4().hex}@example.com"

    # Signup first
    resp = client.post(f"/activities/{urllib.parse.quote(activity)}/signup", params={"email": email})
    assert resp.status_code == 200

    # Now unregister
    resp = client.delete(f"/activities/{urllib.parse.quote(activity)}/unregister", params={"email": email})
    assert resp.status_code == 200, resp.text

    # Immediately fetch activities and confirm participant removed
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert email not in data[activity]["participants"]
