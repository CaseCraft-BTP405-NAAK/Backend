#!/usr/bin/env python3
"""
Add multiple products through the API
"""
import json
import requests
import time

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

# Sample products data
products = [
    {
        "name": "Samsung Galaxy S23 Case",
        "description": "Slim-fit case for Samsung Galaxy S23 with reinforced corners and raised bezels.",
        "price": 24.99,
        "stock": 45,
        "image_url": "https://placehold.co/400x400/purple/white?text=Samsung+Case",
        "category": "Phone Cases",
        "customizable": False
    },
    {
        "name": "Tempered Glass Screen Protector",
        "description": "Ultra-clear 9H hardness tempered glass screen protector with easy installation kit.",
        "price": 14.99,
        "stock": 100,
        "image_url": "https://placehold.co/400x400/blue/white?text=Screen+Protector",
        "category": "Screen Protectors",
        "customizable": False
    },
    {
        "name": "Wireless Charging Pad",
        "description": "Fast 15W wireless charging pad compatible with all Qi-enabled devices.",
        "price": 34.99,
        "stock": 30,
        "image_url": "https://placehold.co/400x400/gray/white?text=Wireless+Charger",
        "category": "Chargers",
        "customizable": False
    },
    {
        "name": "USB-C to Lightning Cable",
        "description": "Durable 6ft braided USB-C to Lightning cable with fast charging support.",
        "price": 19.99,
        "stock": 75,
        "image_url": "https://placehold.co/400x400/black/white?text=USB+Cable",
        "category": "Accessories",
        "customizable": False
    },
    {
        "name": "Laptop Sleeve (Customizable)",
        "description": "Premium protective sleeve for laptops up to 15 inches. Water-resistant material with soft interior lining. Fully customizable with your choice of colors, patterns, and personal touches.",
        "price": 49.99,
        "stock": 35,
        "image_url": "https://placehold.co/400x400/navy/white?text=Laptop+Sleeve",
        "category": "Accessories",
        "customizable": True,
        "customization_options": {
            "colors": [
                {"id": "c1", "name": "Charcoal", "hex": "#36454F", "price_modifier": 0},
                {"id": "c2", "name": "Navy Blue", "hex": "#0a4b76", "price_modifier": 0},
                {"id": "c3", "name": "Olive Green", "hex": "#556b2f", "price_modifier": 0},
                {"id": "c4", "name": "Burgundy", "hex": "#800020", "price_modifier": 0},
                {"id": "c5", "name": "Slate Gray", "hex": "#708090", "price_modifier": 0}
            ],
            "patterns": [
                {"id": "p1", "name": "Minimal", "image_url": "https://placehold.co/100x100/eee/gray?text=Minimal", "price_modifier": 0},
                {"id": "p2", "name": "Geometric", "image_url": "https://placehold.co/100x100/eee/gray?text=Geo", "price_modifier": 8},
                {"id": "p3", "name": "Tech Pattern", "image_url": "https://placehold.co/100x100/eee/gray?text=Tech", "price_modifier": 8},
                {"id": "p4", "name": "Circuit Board", "image_url": "https://placehold.co/100x100/eee/gray?text=Circuit", "price_modifier": 10}
            ],
            "texts": [
                {
                    "id": "t1",
                    "name": "Custom Text",
                    "max_length": 20,
                    "available_fonts": [
                        {"id": "f1", "name": "Sans Serif"},
                        {"id": "f2", "name": "Serif"},
                        {"id": "f3", "name": "Script"},
                        {"id": "f4", "name": "Monospace"}
                    ],
                    "price_modifier": 12
                },
                {
                    "id": "t2",
                    "name": "Monogram",
                    "max_length": 3,
                    "available_fonts": [
                        {"id": "f1", "name": "Classic"},
                        {"id": "f5", "name": "Modern"},
                        {"id": "f6", "name": "Elegant"}
                    ],
                    "price_modifier": 8
                }
            ],
            "images": [
                {
                    "id": "i1",
                    "name": "Custom Image",
                    "max_size_kb": 8000,
                    "allowed_types": ["image/jpeg", "image/png", "image/gif", "image/svg+xml"],
                    "price_modifier": 18
                }
            ]
        }
    }
]

def main():
    """Add products using the API"""
    token = get_admin_token()
    if not token:
        print("Failed to get admin token. Exiting.")
        return
    
    # Add products
    headers = {"Authorization": f"Bearer {token}"}
    
    for i, product in enumerate(products):
        print(f"Adding product {i+1}/{len(products)}: {product['name']}")
        
        response = requests.post(
            f"{API_URL}/api/products", 
            json=product,
            headers=headers
        )
        
        if response.status_code == 200 or response.status_code == 201:
            print(f"Product added successfully: {product['name']}")
        else:
            print(f"Failed to add product: {response.status_code}")
            print(response.text)
        
        # Sleep to avoid hammering the API
        time.sleep(1)
    
    print("All products added!")

if __name__ == "__main__":
    main() 
