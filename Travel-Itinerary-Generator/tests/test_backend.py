"""
Backend API Tests
Tests for FastAPI endpoints and functionality
"""

import pytest
from fastapi.testclient import TestClient
import sys
sys.path.append('.')
from backend.main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "version" in data


def test_generate_itinerary_valid():
    """Test itinerary generation with valid input"""
    payload = {
        "destination": "Manali",
        "budget": 20000,
        "days": 3,
        "include_meals": True,
        "include_hotel": True
    }
    response = client.post("/api/generate-itinerary", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "destination" in data
    assert "duration" in data
    assert "itinerary" in data
    assert "total_cost" in data
    assert len(data["itinerary"]) > 0


def test_generate_itinerary_invalid_destination():
    """Test itinerary generation with empty destination"""
    payload = {
        "destination": "",
        "budget": 20000,
        "days": 3,
        "include_meals": True,
        "include_hotel": True
    }
    response = client.post("/api/generate-itinerary", json=payload)
    assert response.status_code == 422  # Validation error


def test_generate_itinerary_invalid_budget():
    """Test itinerary generation with invalid budget"""
    payload = {
        "destination": "Manali",
        "budget": -100,
        "days": 3,
        "include_meals": True,
        "include_hotel": True
    }
    response = client.post("/api/generate-itinerary", json=payload)
    assert response.status_code == 422  # Validation error


def test_generate_itinerary_invalid_days():
    """Test itinerary generation with invalid days"""
    payload = {
        "destination": "Manali",
        "budget": 20000,
        "days": 0,
        "include_meals": True,
        "include_hotel": True
    }
    response = client.post("/api/generate-itinerary", json=payload)
    assert response.status_code == 422  # Validation error


def test_get_destinations():
    """Test getting popular destinations"""
    response = client.get("/api/destinations")
    assert response.status_code == 200
    data = response.json()
    assert "destinations" in data
    assert isinstance(data["destinations"], list)


def test_budget_constraint():
    """Test that budget constraint is enforced"""
    payload = {
        "destination": "Manali",
        "budget": 5000,  # Low budget
        "days": 3,
        "include_meals": True,
        "include_hotel": True
    }
    response = client.post("/api/generate-itinerary", json=payload)
    assert response.status_code == 200
    data = response.json()
    # Total cost should not exceed budget
    assert data["total_cost"] <= payload["budget"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
