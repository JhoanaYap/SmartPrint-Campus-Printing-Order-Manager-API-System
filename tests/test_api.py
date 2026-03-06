from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_and_get_order():
    resp = client.post("/orders", json={"client_name": "Test User", "pages": 3, "paper_type": "black_white"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_cost"] == 6.0
    oid = data["id"]

    r2 = client.get(f"/orders/{oid}")
    assert r2.status_code == 200
    assert r2.json()["id"] == oid
