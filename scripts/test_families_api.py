#!/usr/bin/env python3
"""
Test the /products/api/families endpoint and print the result.
"""
import requests

API_URL = "http://localhost:8000/products/api/families"

# If you need to test with authentication, set your session cookie here
SESSION_COOKIE = None  # e.g. 'your-session-cookie-value'

headers = {}
cookies = {}
if SESSION_COOKIE:
    cookies['session'] = SESSION_COOKIE

try:
    print(f"Requesting: {API_URL}")
    response = requests.get(API_URL, headers=headers, cookies=cookies)
    print(f"Status code: {response.status_code}")
    print("Response body:")
    print(response.text)
except Exception as e:
    print(f"Error: {e}")
