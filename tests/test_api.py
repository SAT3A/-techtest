from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_predict_positive(client):
    text = "The product is amazing and works perfectly!"
    response = client.post("/predict", json={"text": text})
    body = response.json()

    assert response.status_code == 200
    assert body["text"] == text
    assert body["sentiment"] == "positive"
    assert 0.0 <= body["confidence"] <= 1.0


def test_predict_negative(client):
    response = client.post(
        "/predict",
        json={"text": "Terrible quality, it broke after one day."},
    )
    body = response.json()

    assert response.status_code == 200
    assert body["sentiment"] == "negative"


def test_predict_strips_whitespace(client):
    response = client.post("/predict", json={"text": "   good product   "})
    assert response.status_code == 200
    assert response.json()["text"] == "good product"


def test_predict_blank_text_returns_422(client):
    response = client.post("/predict", json={"text": "   "})
    assert response.status_code == 422


def test_predict_missing_text_returns_422(client):
    response = client.post("/predict", json={})
    assert response.status_code == 422


def test_predict_too_long_returns_422(client):
    response = client.post("/predict", json={"text": "a" * 5001})
    assert response.status_code == 422
