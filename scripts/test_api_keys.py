#!/usr/bin/env python3
"""
InvoicePlanePy API Test Script

This script demonstrates how to use API keys to access InvoicePlanePy APIs.
Run this after generating an API key from the web interface.
"""

import requests
import json
import sys

# Configuration
BASE_URL = "http://localhost:8000"
API_KEY = "sk_your_api_key_here"  # Replace with your actual API key

def test_api_key_auth():
    """Test API key authentication with invoices endpoint"""
    print("🔑 Testing API Key Authentication...")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(f"{BASE_URL}/invoices/api?page=1&limit=5", headers=headers)

        if response.status_code == 401:
            print("❌ Authentication failed - check your API key")
            return False
        elif response.status_code == 200:
            data = response.json()
            print(f"✅ Authentication successful!")
            print(f"📄 Found {data['pagination']['total']} total invoices")
            print(f"📋 Returned {len(data['invoices'])} invoices in this page")
            return True
        else:
            print(f"❌ Unexpected response: {response.status_code}")
            print(response.text)
            return False

    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - is InvoicePlanePy running?")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_other_endpoints():
    """Test other API endpoints"""
    print("\n🧪 Testing other API endpoints...")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    endpoints = [
        ("Products", f"{BASE_URL}/products/api?page=1&limit=5"),
        ("Payments", f"{BASE_URL}/payments/api?page=1&limit=5"),
        ("Tax Rates", f"{BASE_URL}/tax_rates/api"),
    ]

    for name, url in endpoints:
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                print(f"✅ {name} API: OK")
            else:
                print(f"⚠️  {name} API: {response.status_code}")
        except Exception as e:
            print(f"❌ {name} API: Error - {e}")

def main():
    print("🚀 InvoicePlanePy API Test Script")
    print("=" * 40)

    if API_KEY == "sk_your_api_key_here":
        print("⚠️  Please set your API key in the API_KEY variable at the top of this script")
        print("   Generate an API key from: http://localhost:8000/settings/api-keys")
        sys.exit(1)

    # Test authentication
    if test_api_key_auth():
        # Test other endpoints
        test_other_endpoints()
        print("\n🎉 All tests completed!")
    else:
        print("\n❌ Authentication test failed - check your setup")

if __name__ == "__main__":
    main()