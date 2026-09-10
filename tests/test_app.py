import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health(client):
    response = client.get("/health")
    data = response.get_json()

    assert response.status_code == 200
    assert data["status"] == "healthy"
    assert data["application"] == "student-ml-api"


def test_predict_success(client):
    response = client.post("/predict", json={"value": 10})
    data = response.get_json()

    assert response.status_code == 200
    assert data["input"] == 10
    assert data["prediction"] == 20


def test_predict_missing_input(client):
    response = client.post("/predict", json={})
    data = response.get_json()

    assert response.status_code == 400
    assert "error" in data


def test_predict_invalid_input(client):
    response = client.post("/predict", json={"value": "not_a_number"})
    data = response.get_json()

    assert response.status_code == 400
    assert "error" in data