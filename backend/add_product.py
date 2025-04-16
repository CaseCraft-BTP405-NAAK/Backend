#!/usr/bin/env python3
"""
Add a single product through the API
"""
import json
import requests

# API URL
API_URL = "http://localhost:8000"

# Admin login
def get_admin_token():
    """Get admin token for API requests"""
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    response = requests.post(
        f"{API_URL}/api/auth/token", 
        data=login_data
    )
    
    if response.status_code != 200:
        print(f"Login failed: {response.text}")
        return None
    
    token_data = response.json()
    return token_data["access_token"]

# Sample product data
product = {
    "name": "iPhone 14 Pro Case (Customizable)",
    "description": "Premium protective case for iPhone 14 Pro with MagSafe compatibility and drop protection. Customize with your favorite colors, patterns, and even add personal text or images!",
    "price": 39.99,
    "stock": 50,
    "image_url": "https://placehold.co/400x400/indigo/white?text=iPhone+Case",
    "category": "Phone Cases",
    "customizable": True,
    "customization_options": {
        "colors": [
            {"id": "c1", "name": "Matte Black", "hex": "#252525", "price_modifier": 0},
            {"id": "c2", "name": "Navy Blue", "hex": "#0a4b76", "price_modifier": 0},
            {"id": "c3", "name": "Forest Green", "hex": "#1e4d2b", "price_modifier": 0},
            {"id": "c4", "name": "Burgundy", "hex": "#800020", "price_modifier": 0},
            {"id": "c5", "name": "Clear", "hex": "#f5f5f5", "price_modifier": -5},
            {"id": "c6", "name": "Rose Gold", "hex": "#ebc2c0", "price_modifier": 5}
        ],
        "patterns": [
            {"id": "p1", "name": "Minimal", "image_url": "https://placehold.co/100x100/eee/gray?text=Minimal", "price_modifier": 0},
            {"id": "p2", "name": "Geometric", "image_url": "https://placehold.co/100x100/eee/gray?text=Geo", "price_modifier": 5},
            {"id": "p3", "name": "Abstract", "image_url": "https://placehold.co/100x100/eee/gray?text=Abstract", "price_modifier": 5},
            {"id": "p4", "name": "Marble", "image_url": "https://placehold.co/100x100/eee/gray?text=Marble", "price_modifier": 8}
        ],
        "texts": [
            {
                "id": "t1",
                "name": "Custom Text",
                "max_length": 15,
                "available_fonts": [
                    {"id": "f1", "name": "Sans Serif"},
                    {"id": "f2", "name": "Serif"},
                    {"id": "f3", "name": "Script"},
                    {"id": "f4", "name": "Monospace"}
                ],
                "price_modifier": 10
            }
        ],
        "images": [
            {
                "id": "i1",
                "name": "Custom Image",
                "max_size_kb": 5000,
                "allowed_types": ["image/jpeg", "image/png", "image/gif"],
                "price_modifier": 15
            }
        ]
    }
}

def main():
    """Add a product using the API"""
    token = get_admin_token()
    if not token:
        print("Failed to get admin token. Exiting.")
        return
    
    # Print API endpoints
    response = requests.get(f"{API_URL}/")
    print(f"API response: {response.text}")
    
    # Add product
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        f"{API_URL}/api/products", 
        json=product,
        headers=headers
    )
    
    if response.status_code == 200 or response.status_code == 201:
        print(f"Product added successfully: {response.json()}")
    else:
        print(f"Failed to add product: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    main() 
