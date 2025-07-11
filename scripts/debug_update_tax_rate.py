#!/usr/bin/env python3
"""
Enhanced Tax Rate API Debug Script - 422 Error Analysis

This script helps debug the 422 Unprocessable Entity error by:
1. Testing different payload formats
2. Examining API schema/documentation
3. Providing detailed error analysis
"""

import requests
import json
import sys
from typing import Dict, Any, Optional


class TaxRateDebugger:
    """Debug 422 errors in tax rate API endpoints."""
    
    def __init__(self, base_url: str, session: requests.Session):
        self.base_url = base_url.rstrip('/')
        self.session = session
        self.api_url = f"{base_url}/tax_rates/api"
        self.save_url = f"{base_url}/tax_rates/api/save"
        
    def test_different_payloads(self) -> None:
        """Test various payload formats to identify the correct one."""
        print("\n🔍 Testing different payload formats...")
        
        # Test cases with different payload structures
        test_cases = [
            {
                "name": "Direct object",
                "payload": {"name": "DebugTest", "rate": 42.0},
                "description": "Simple tax rate object"
            },
            {
                "name": "Wrapped in tax_rate",
                "payload": {"tax_rate": {"name": "DebugTest", "rate": 42.0}},
                "description": "Tax rate wrapped in tax_rate key"
            },
            {
                "name": "With additional fields",
                "payload": {
                    "name": "DebugTest", 
                    "rate": 42.0,
                    "description": "Test tax rate",
                    "active": True
                },
                "description": "Tax rate with extra fields"
            },
            {
                "name": "Rate as string",
                "payload": {"name": "DebugTest", "rate": "42.0"},
                "description": "Rate as string instead of float"
            },
            {
                "name": "Rate as integer",
                "payload": {"name": "DebugTest", "rate": 42},
                "description": "Rate as integer instead of float"
            },
            {
                "name": "Different field names",
                "payload": {"tax_name": "DebugTest", "tax_rate": 42.0},
                "description": "Alternative field names"
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n📋 Test {i}: {test_case['name']}")
            print(f"   Description: {test_case['description']}")
            print(f"   Payload: {json.dumps(test_case['payload'], indent=2)}")
            
            response = self._make_request('POST', self.api_url, json=test_case['payload'])
            
            if response and response.status_code == 200:
                print(f"   ✅ SUCCESS! This payload format works")
                return test_case['payload']
            else:
                self._analyze_error_response(response)
        
        print("\n❌ None of the test payloads worked")
        return None
    
    def check_api_documentation(self) -> None:
        """Check if API provides OpenAPI documentation."""
        print("\n📚 Checking API documentation...")
        
        # Try common FastAPI documentation endpoints
        doc_endpoints = [
            ("/docs", "Swagger UI"),
            ("/redoc", "ReDoc"),
            ("/openapi.json", "OpenAPI Schema")
        ]
        
        for endpoint, name in doc_endpoints:
            url = f"{self.base_url}{endpoint}"
            try:
                response = self.session.get(url, timeout=10)
                if response.status_code == 200:
                    print(f"✅ {name} available at: {url}")
                    if endpoint == "/openapi.json":
                        self._analyze_openapi_schema(response.json())
                else:
                    print(f"❌ {name} not available at: {url}")
            except Exception as e:
                print(f"❌ Error accessing {name}: {e}")
    
    def _analyze_openapi_schema(self, schema: Dict[str, Any]) -> None:
        """Analyze OpenAPI schema for tax rate endpoints."""
        print("\n🔍 Analyzing OpenAPI schema for tax rate endpoints...")
        
        paths = schema.get("paths", {})
        components = schema.get("components", {})
        
        # Look for tax rate related endpoints
        tax_rate_paths = {
            path: details for path, details in paths.items() 
            if "tax_rate" in path.lower()
        }
        
        if tax_rate_paths:
            print(f"Found {len(tax_rate_paths)} tax rate endpoints:")
            for path, details in tax_rate_paths.items():
                print(f"\n📍 {path}:")
                for method, method_details in details.items():
                    if method.upper() in ['GET', 'POST', 'PUT', 'DELETE']:
                        print(f"   {method.upper()}: {method_details.get('summary', 'No summary')}")
                        
                        # Check request body schema
                        if 'requestBody' in method_details:
                            request_body = method_details['requestBody']
                            content = request_body.get('content', {})
                            if 'application/json' in content:
                                schema_ref = content['application/json'].get('schema', {})
                                print(f"   Request Schema: {json.dumps(schema_ref, indent=6)}")
        
        # Look for tax rate models in components
        schemas = components.get("schemas", {})
        tax_rate_schemas = {
            name: schema for name, schema in schemas.items()
            if "tax" in name.lower() or "rate" in name.lower()
        }
        
        if tax_rate_schemas:
            print(f"\n📋 Found {len(tax_rate_schemas)} tax rate related schemas:")
            for name, schema in tax_rate_schemas.items():
                print(f"\n🏷️  {name}:")
                properties = schema.get("properties", {})
                required = schema.get("required", [])
                
                for prop_name, prop_details in properties.items():
                    prop_type = prop_details.get("type", "unknown")
                    is_required = prop_name in required
                    print(f"   - {prop_name}: {prop_type} {'(required)' if is_required else '(optional)'}")
    
    def _make_request(self, method: str, url: str, **kwargs) -> Optional[requests.Response]:
        """Make HTTP request with the authenticated session."""
        try:
            response = self.session.request(method, url, timeout=10, **kwargs)
            return response
        except Exception as e:
            print(f"   ❌ Request failed: {e}")
            return None
    
    def _analyze_error_response(self, response: Optional[requests.Response]) -> None:
        """Analyze error response for detailed information."""
        if not response:
            print("   ❌ No response received")
            return
        
        print(f"   ❌ Status: {response.status_code}")
        
        # Try to get detailed error information
        try:
            error_data = response.json()
            print(f"   📋 Response: {json.dumps(error_data, indent=6)}")
            
            # FastAPI validation errors usually contain 'detail' field
            if 'detail' in error_data:
                detail = error_data['detail']
                if isinstance(detail, list):
                    print("   🔍 Validation errors:")
                    for error in detail:
                        if isinstance(error, dict):
                            loc = error.get('loc', [])
                            msg = error.get('msg', 'Unknown error')
                            error_type = error.get('type', 'Unknown type')
                            print(f"      - Field: {'.'.join(map(str, loc))}")
                            print(f"        Error: {msg}")
                            print(f"        Type: {error_type}")
                else:
                    print(f"   📋 Detail: {detail}")
        except Exception as e:
            print(f"   ❌ Could not parse response as JSON: {e}")
            print(f"   📋 Raw response: {response.text[:500]}...")
    
    def compare_working_vs_failing(self) -> None:
        """Compare working bulk save vs failing individual create."""
        print("\n🔄 Comparing working vs failing operations...")
        
        # Get current tax rates (this works)
        print("\n✅ Working operation - GET tax rates:")
        response = self._make_request('GET', self.api_url)
        if response and response.status_code == 200:
            current_rates = response.json()
            print(f"   Response: {json.dumps(current_rates, indent=6)}")
            
            if current_rates:
                print(f"\n📋 Structure of existing tax rate:")
                first_rate = current_rates[0]
                print(f"   Fields: {list(first_rate.keys())}")
                print(f"   Types: {[(k, type(v).__name__) for k, v in first_rate.items()]}")
                
                # Try to create a tax rate with the same structure
                print(f"\n🔄 Attempting to create tax rate with same structure...")
                test_payload = {
                    key: f"DebugTest" if isinstance(value, str) else 42.0 if isinstance(value, (int, float)) else value
                    for key, value in first_rate.items()
                }
                # Override with test values
                if 'name' in test_payload:
                    test_payload['name'] = 'DebugTest'
                if 'rate' in test_payload:
                    test_payload['rate'] = 42.0
                
                print(f"   Test payload: {json.dumps(test_payload, indent=6)}")
                response = self._make_request('POST', self.api_url, json=test_payload)
                self._analyze_error_response(response)
    
    def run_debug_analysis(self) -> None:
        """Run comprehensive debug analysis."""
        print("🔍 Starting comprehensive 422 error analysis...")
        print("=" * 60)
        
        # Step 1: Check API documentation
        self.check_api_documentation()
        
        # Step 2: Compare working vs failing operations
        self.compare_working_vs_failing()
        
        # Step 3: Test different payload formats
        self.test_different_payloads()
        
        print("\n" + "=" * 60)
        print("🎯 Debug analysis complete!")
        print("\n💡 Recommendations:")
        print("1. Check the OpenAPI schema at /docs or /openapi.json")
        print("2. Compare the structure of existing tax rates with your payload")
        print("3. Ensure all required fields are included")
        print("4. Verify data types match the API expectations")
        print("5. Check if the API expects different field names")


def main():
    """Main debug function."""
    import os
    
    # Configuration
    base_url = os.environ.get("BASE_URL", "http://simple.local:8080")
    username = os.environ.get("USERNAME", "admin")
    password = os.environ.get("PASSWORD", "admin")
    
    print("🔍 Tax Rate API 422 Error Debug Analysis")
    print("=" * 50)
    print(f"Base URL: {base_url}")
    print(f"Username: {username}")
    print("=" * 50)
    
    # Create session and login
    session = requests.Session()
    
    print("🔐 Logging in...")
    login_data = {"username": username, "password": password}
    login_response = session.post(
        f"{base_url}/auth/login",
        data=login_data,
        timeout=10
    )
    
    if login_response.status_code == 200:
        print("✅ Login successful")
        
        # Run debug analysis
        debugger = TaxRateDebugger(base_url, session)
        debugger.run_debug_analysis()
    else:
        print(f"❌ Login failed: {login_response.status_code}")
        if login_response.text:
            print(f"Response: {login_response.text}")
        sys.exit(1)


if __name__ == "__main__":
    main()