import pytest
from fastapi.testclient import TestClient
from app import app, employees, next_id

client = TestClient(app)

def reset_employees():
    employees.clear()
    employees.extend([
        {"id": 1, "name":"John Doe","email":"john.doe@company.com","department":"Engineering","position":"Software Engineer","status":"Active"},
        {"id": 2, "name":"Jane Smith","email":"jane.smith@company.com","department":"Marketing","position":"Marketing Manager","status":"Active"},
        {"id": 3, "name":"Robert Johnson","email":"robert.johnson@company.com","department":"Engineering","position":"DevOps Engineer","status":"On Leave"},
    ])
    import app as app_module
    app_module.next_id = 4

@pytest.fixture(autouse=True)
def setup():
    reset_employees()
    yield

def test_get_employees():
    resp = client.get("/employees")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 3
    assert data[0]["name"] == "John Doe"

def test_create_employee():
    payload = {"name":"Alice","email":"alice@company.com","department":"HR","position":"Recruiter","status":"Active"}
    resp = client.post("/employees", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Alice"
    assert data["id"] >= 4

def test_create_employee_missing_email():
    payload = {"name":"Alice","department":"HR"}
    resp = client.post("/employees", json=payload)
    assert resp.status_code == 422

def test_create_employee_missing_department():
    payload = {"name":"Alice","email":"alice@company.com"}
    resp = client.post("/employees", json=payload)
    assert resp.status_code == 422

def test_get_employee_not_found():
    resp = client.get("/employees/999")
    assert resp.status_code == 404

def test_update_employee():
    payload = {"name":"John Updated","email":"john@company.com","department":"Engineering","position":"Senior Engineer","status":"Active"}
    resp = client.put("/employees/1", json=payload)
    assert resp.status_code == 200
    assert resp.json()["name"] == "John Updated"

def test_delete_employee():
    resp = client.delete("/employees/2")
    assert resp.status_code == 204
    resp2 = client.get("/employees")
    assert len(resp2.json()) == 2

def test_delete_employee_not_found():
    resp = client.delete("/employees/999")
    assert resp.status_code == 404
