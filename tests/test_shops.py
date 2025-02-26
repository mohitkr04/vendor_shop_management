from urllib.parse import urlencode
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app import schemas
import json

def test_create_shop(client: TestClient, test_db: Session):
    # First, create and log in a vendor
    vendor_data = {
        "name": "Shop Vendor",
        "email": "shop@example.com",
        "password": "password123"
    }
    vendor_response = client.post("/vendors/", json=vendor_data)
    assert vendor_response.status_code == 200
    
    # Login to get the token
    login_data = {
        "username": vendor_data["email"],
        "password": vendor_data["password"],
        "grant_type": "password"
    }
    
    login_response = client.post(
        "/vendors/token",
        data=urlencode(login_data),
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert login_response.status_code == 200, f"Login failed: {login_response.text}"
    token = login_response.json()["access_token"]
    
    # Create a shop
    shop_data = {
        "name": "Test Shop",
        "owner": "Shop Owner",
        "business_type": "Retail",
        "latitude": 40.7128,
        "longitude": -74.0060
    }
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = client.post("/shops/", json=shop_data, headers=headers)
    assert response.status_code == 200, f"Shop creation failed: {response.text}"
    data = response.json()
    assert data["name"] == shop_data["name"]
    assert "id" in data

def test_read_shops(client: TestClient, test_db: Session):
    # First create a vendor and a shop
    vendor_data = {
        "name": "Shop Vendor",
        "email": "shopread@example.com",
        "password": "password123"
    }
    vendor_response = client.post("/vendors/", json=vendor_data)
    assert vendor_response.status_code == 200
    
    # Login
    login_data = {
        "username": vendor_data["email"],
        "password": vendor_data["password"],
        "grant_type": "password"
    }
    login_response = client.post(
        "/vendors/token",
        data=urlencode(login_data),
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    token = login_response.json()["access_token"]
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Create a shop
    shop_data = {
        "name": "Test Shop",
        "owner": "Shop Owner",
        "business_type": "Retail",
        "latitude": 40.7128,
        "longitude": -74.0060
    }
    create_response = client.post("/shops/", json=shop_data, headers=headers)
    shop_id = create_response.json()["id"]
    
    # Test reading all shops
    response = client.get("/shops/")
    assert response.status_code == 200
    shops = response.json()
    assert len(shops) > 0
    
    # Test reading specific shop
    response = client.get(f"/shops/{shop_id}")
    assert response.status_code == 200
    assert response.json()["name"] == shop_data["name"]

def test_update_shop(client: TestClient, test_db: Session):
    # Create vendor and shop (similar setup as above)
    # ... setup code ...
    
    # Update shop
    updated_data = {
        "name": "Updated Shop",
        "owner": "New Owner",
        "business_type": "Services",
        "latitude": 40.7128,
        "longitude": -74.0060
    }
    response = client.put(f"/shops/{shop_id}", json=updated_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == updated_data["name"]

def test_delete_shop(client: TestClient, test_db: Session):
    # Create vendor and shop (similar setup as above)
    # ... setup code ...
    
    # Delete shop
    response = client.delete(f"/shops/{shop_id}", headers=headers)
    assert response.status_code == 204
    
    # Verify shop is deleted
    response = client.get(f"/shops/{shop_id}")
    assert response.status_code == 404

def test_nearby_shops(client: TestClient, test_db: Session):
    # Create some shops at known locations
    # ... setup code ...
    
    # Search for nearby shops
    response = client.get("/shops/nearby/", params={
        "latitude": 40.7128,
        "longitude": -74.0060,
        "radius": 1.0
    })
    assert response.status_code == 200
    shops = response.json()
    assert len(shops) > 0

#Add tests for read, update and delete