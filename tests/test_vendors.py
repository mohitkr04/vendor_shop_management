from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app import schemas
import json

def test_create_vendor(client: TestClient, test_db: Session):
    vendor_data = {
        "name": "Test Vendor",
        "email": "test@example.com",
        "password": "password123"
    }
    response = client.post("/vendors/", json=vendor_data)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == vendor_data["email"]
    assert data["name"] == vendor_data["name"]
    assert "id" in data

def test_login_vendor(client: TestClient, test_db: Session):
    # First create a vendor
    vendor_data = {
        "name": "Test Vendor",
        "email": "testlogin@example.com",
        "password": "password123"
    }
    client.post("/vendors/", json=vendor_data)
    
    # Then try to login
    login_data = {
        "username": vendor_data["email"],
        "password": vendor_data["password"]
    }
    response = client.post("/vendors/token", data=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"