"""
Test client for the EventHub AI API integrated features.
This script demonstrates how to call the dynamic pricing API within the integrated application.
"""

import requests
import json

# Base URL of the integrated API
BASE_URL = "http://localhost:8000"

def test_pricing_endpoint():
    """
    Test the dynamic pricing endpoint
    """
    url = f"{BASE_URL}/pricing/adjust-price"
    
    # USA profile (expect higher price)
    usa_payload = {
        "latitude": 38.96, 
        "longitude": -95.71,
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "base_price": 100.0,
        "device_pixel_ratio": "1.5"
    }
    
    # Asia profile (expect standard price)
    asia_payload = {
        "latitude": 34.0, 
        "longitude": 100.0,
        "user_agent": "Mozilla/5.0 (Linux; Android 11; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36",
        "base_price": 100.0,
        "device_pixel_ratio": "2.5"
    }
    
    # Africa profile (expect lower price)
    africa_payload = {
        "latitude": 0.0, 
        "longitude": 25.0,
        "user_agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.127 Mobile Safari/537.36",
        "base_price": 100.0,
        "device_pixel_ratio": "1.0"
    }
    
    print("\n--- Testing Dynamic Pricing API ---")
    
    # Test USA profile
    response = requests.post(url, json=usa_payload)
    if response.status_code == 200:
        result = response.json()
        print(f"USA profile: Original price ${result['original_price']}, Adjusted price ${result['adjusted_price']}")
        print(f"Assigned to cluster: {result['cluster_assigned']}")
    else:
        print(f"Error testing USA profile: {response.status_code} - {response.text}")
    
    # Test Asia profile
    response = requests.post(url, json=asia_payload)
    if response.status_code == 200:
        result = response.json()
        print(f"Asia profile: Original price ${result['original_price']}, Adjusted price ${result['adjusted_price']}")
        print(f"Assigned to cluster: {result['cluster_assigned']}")
    else:
        print(f"Error testing Asia profile: {response.status_code} - {response.text}")
    
    # Test Africa profile
    response = requests.post(url, json=africa_payload)
    if response.status_code == 200:
        result = response.json()
        print(f"Africa profile: Original price ${result['original_price']}, Adjusted price ${result['adjusted_price']}")
        print(f"Assigned to cluster: {result['cluster_assigned']}")
    else:
        print(f"Error testing Africa profile: {response.status_code} - {response.text}")

def test_root_endpoint():
    """
    Test the root endpoint
    """
    url = BASE_URL
    response = requests.get(url)
    if response.status_code == 200:
        print("\n--- API Root Endpoint ---")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error testing root endpoint: {response.status_code} - {response.text}")

if __name__ == "__main__":
    test_root_endpoint()
    test_pricing_endpoint()
    print("\nTest complete. Check the API server logs for more details.")
