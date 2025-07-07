#!/usr/bin/env python3
"""
FastAPI Route Testing Script
This script will help diagnose routing issues in your FastAPI application.
"""

import requests
import json
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:8080"  # Updated to match docker-compose port
TEST_CREDENTIALS = {
    "username": "admin",
    "password": "admin123"
}

def test_route_exists(method: str, path: str) -> Dict[str, Any]:
    """Test if a route exists and what response it gives"""
    url = f"{BASE_URL}{path}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, allow_redirects=False)
        elif method.upper() == "POST":
            response = requests.post(url, data=TEST_CREDENTIALS, allow_redirects=False)
        else:
            return {"error": f"Unsupported method: {method}"}
        
        return {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "content": response.text[:500] if response.text else None,  # First 500 chars
            "redirects_to": response.headers.get("location") if response.status_code in [301, 302, 307, 308] else None
        }
    except requests.exceptions.ConnectionError:
        return {"error": "Connection failed - is your FastAPI app running?"}
    except Exception as e:
        return {"error": str(e)}

def get_fastapi_routes():
    """Try to get route information from FastAPI app if available"""
    try:
        # This assumes your FastAPI app has a debug endpoint
        response = requests.get(f"{BASE_URL}/debug/routes")
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def main():
    print("🔍 FastAPI Route Testing Script")
    print("=" * 50)
    
    # Test the routes we expect to exist
    routes_to_test = [
        ("GET", "/"),
        ("GET", "/auth/login"),
        ("POST", "/auth/login"),
        ("POST", "/login"),  # Alternative route
        ("GET", "/dashboard"),
        ("GET", "/favicon.ico"),
    ]
    
    print(f"Testing against: {BASE_URL}")
    print("-" * 50)
    
    for method, path in routes_to_test:
        print(f"\n📍 Testing {method} {path}")
        result = test_route_exists(method, path)
        
        if "error" in result:
            print(f"   ❌ {result['error']}")
        else:
            status = result["status_code"]
            if status == 200:
                print(f"   ✅ {status} OK")
            elif status == 302:
                print(f"   🔄 {status} Redirect to: {result['redirects_to']}")
            elif status == 404:
                print(f"   ❌ {status} Not Found")
            else:
                print(f"   ⚠️  {status} {requests.status_codes._codes.get(status, ['Unknown'])[0]}")
            
            # Show content preview for errors
            if status >= 400 and result.get("content"):
                print(f"   📝 Content preview: {result['content'][:100]}...")

    # Test login form submission specifically
    print("\n" + "=" * 50)
    print("🔐 Testing Login Form Submission")
    print("=" * 50)
    
    # Test the exact form submission
    form_data = {
        "username": TEST_CREDENTIALS["username"],
        "password": TEST_CREDENTIALS["password"]
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            data=form_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            allow_redirects=False
        )
        
        print(f"Form submission result:")
        print(f"  Status: {response.status_code}")
        print(f"  Headers: {dict(response.headers)}")
        
        if response.status_code == 302:
            print(f"  ✅ Redirect to: {response.headers.get('location')}")
        elif response.status_code == 404:
            print(f"  ❌ Route not found - you need to add POST /auth/login")
        else:
            print(f"  Content: {response.text[:200]}...")
            
    except Exception as e:
        print(f"  ❌ Error: {e}")

    # Additional debugging info
    print("\n" + "=" * 50)
    print("🛠️  Debugging Information")
    print("=" * 50)
    
    print("\nBased on your HTML form:")
    print("  Form action: /auth/login")
    print("  Form method: POST")
    print("  Expected fields: username, password")
    
    print("\nWhat your FastAPI app should have:")
    print("  @app.get('/auth/login')   # Show login form")
    print("  @app.post('/auth/login')  # Process login form")
    
    print("\nQuick fix commands:")
    print("  1. Check your routes: docker logs <container_id> | grep 'GET\\|POST'")
    print("  2. Add missing route in your FastAPI app")
    print("  3. Restart your container")

if __name__ == "__main__":
    main()