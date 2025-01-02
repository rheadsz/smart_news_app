# tests/test_main.py

import pytest
from fastapi.testclient import TestClient
from services.news_service.main import app  # Adjust the import based on your project structure

client = TestClient(app)

def test_get_news():
    response = client.get("/api/news")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Ensure it returns a list of articles

def test_get_news_by_category():
    response = client.get("/api/news?category=business")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_categories():
    response = client.get("/api/categories")
    assert response.status_code == 200
    assert "business" in response.json()  # Adjust based on your actual categories

def test_get_article():
    response = client.get("/api/news/1")  # Replace with a valid article ID
    assert response.status_code == 200
    assert "title" in response.json()  # Ensure the article has a title