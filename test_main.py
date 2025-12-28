import pytest
from fastapi.testclient import TestClient
from main import app, RootCauseAnalysis

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "AI Customer Support Root Cause Analyzer is running!"}

def test_analyze_ticket_endpoint():
    test_ticket = "Subject: My account is locked\n\nI can't access my account. It says it's locked." # Using a simple ticket for testing
    response = client.post("/analyze_ticket", json={"ticket": test_ticket})
    assert response.status_code == 200
    analysis = RootCauseAnalysis(**response.json())

    assert analysis.summary != ""
    assert analysis.category != ""
    assert analysis.root_cause != ""
    assert analysis.issue_type in ["Bug", "UX gap", "Performance", "Misconfiguration", "User error"]
    assert analysis.severity in ["High", "Medium", "Low"]
    assert 0.0 <= analysis.confidence <= 1.0
    assert isinstance(analysis.engineering_actions, list)
    assert isinstance(analysis.product_actions, list)
    assert analysis.support_reply_suggestion != ""
    assert isinstance(analysis.similar_incidents, list)

    # Test with an empty ticket (should still return a valid structure, but potentially generic)
    response_empty = client.post("/analyze_ticket", json={"ticket": ""})
    assert response_empty.status_code == 200
    analysis_empty = RootCauseAnalysis(**response_empty.json())
    assert analysis_empty.summary != ""
