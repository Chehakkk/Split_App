#!/usr/bin/env python3
"""
Test script to verify Django API endpoints are working
Run this after starting the Django server
"""

import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_api_endpoints():
    """Test all API endpoints"""
    
    print("Testing Django API endpoints...")
    print("=" * 50)
    
    # Test groups endpoint
    try:
        print("Testing /groups/ endpoint...")
        response = requests.get(f"{BASE_URL}/groups/")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error testing groups: {e}")
    
    print("-" * 30)
    
    # Test categories endpoint
    try:
        print("Testing /categories/ endpoint...")
        response = requests.get(f"{BASE_URL}/categories/")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error testing categories: {e}")
    
    print("-" * 30)
    
    # Test expenses endpoint
    try:
        print("Testing /expenses/ endpoint...")
        response = requests.get(f"{BASE_URL}/expenses/")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error testing expenses: {e}")
    
    print("-" * 30)
    
    # Test payments endpoint
    try:
        print("Testing /payments/ endpoint...")
        response = requests.get(f"{BASE_URL}/payments/")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error testing payments: {e}")

if __name__ == "__main__":
    test_api_endpoints() 