"""
Backend API Tests
Tests for FastAPI endpoints and core functionality.
Run from the project root: pytest tests/ -v
"""

import pytest
import sys
import os

# Ensure project root is on the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


# ── Health ─────────────────────────────────────────────────────────────────

def test_health_check():
    """Health check endpoint returns 200 and correct structure."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "version" in data


# ── Destinations ───────────────────────────────────────────────────────────

def test_get_destinations():
    """Popular destinations endpoint returns a list."""
    response = client.get("/api/destinations")
    assert response.status_code == 200
    data = response.json()
    assert "destinations" in data
    assert isinstance(data["destinations"], list)
    assert len(data["destinations"]) > 0


# ── Itinerary Generation ───────────────────────────────────────────────────

VALID_PAYLOAD = {
    "destination": "Goa",
    "budget": "20000 INR",
    "days": 3,
    "mode": "seasonal",
    "starting_place": "Mumbai",
    "people_count": 2,
    "interests": ["beach", "food"],
    "accommodation_type": "Mid-range",
    "notes": "Vegetarian food preferred",
    "include_meals": True,
    "include_hotel": True,
}


def test_generate_itinerary_valid():
    """Valid payload should return a complete itinerary."""
    response = client.post("/api/generate-itinerary", json=VALID_PAYLOAD)
    assert response.status_code == 200
    data = response.json()
    assert "destination" in data
    assert "duration" in data
    assert "itinerary" in data
    assert "total_cost" in data
    assert isinstance(data["itinerary"], list)
    assert len(data["itinerary"]) > 0


def test_generate_itinerary_correct_day_count():
    """Returned itinerary should have exactly the requested number of days."""
    payload = {**VALID_PAYLOAD, "days": 4}
    response = client.post("/api/generate-itinerary", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data["itinerary"]) == 4


def test_generate_itinerary_surprise_mode():
    """Surprise mode should work with empty destination."""
    payload = {**VALID_PAYLOAD, "mode": "surprise", "destination": ""}
    response = client.post("/api/generate-itinerary", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["destination"] != ""  # Should have been auto-assigned


def test_generate_itinerary_missing_budget():
    """Request without budget should fail validation."""
    payload = {k: v for k, v in VALID_PAYLOAD.items() if k != "budget"}
    response = client.post("/api/generate-itinerary", json=payload)
    assert response.status_code == 422


def test_generate_itinerary_invalid_days_zero():
    """Days=0 should fail validation."""
    payload = {**VALID_PAYLOAD, "days": 0}
    response = client.post("/api/generate-itinerary", json=payload)
    assert response.status_code == 422


def test_generate_itinerary_invalid_days_over_limit():
    """Days>30 should fail validation."""
    payload = {**VALID_PAYLOAD, "days": 31}
    response = client.post("/api/generate-itinerary", json=payload)
    assert response.status_code == 422


def test_generate_itinerary_empty_destination_non_surprise():
    """Empty destination in non-surprise mode should fail."""
    payload = {**VALID_PAYLOAD, "destination": "", "mode": "seasonal"}
    response = client.post("/api/generate-itinerary", json=payload)
    assert response.status_code == 422


def test_itinerary_has_day_slots():
    """Each day in the itinerary should have morning, afternoon, evening keys."""
    response = client.post("/api/generate-itinerary", json=VALID_PAYLOAD)
    assert response.status_code == 200
    data = response.json()
    for day in data["itinerary"]:
        assert "day" in day
        # At least one of the time slots must be present
        has_slot = any(day.get(s) for s in ("morning", "afternoon", "evening"))
        assert has_slot, f"Day {day.get('day')} has no time slots"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
