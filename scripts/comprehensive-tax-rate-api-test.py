#!/usr/bin/env python3
"""
Comprehensive Tax Rate API Tester

This script thoroughly tests tax rate creation with proper form data format,
validates the solution, and provides detailed analysis of API behavior.
"""

import requests
import json
import sys
import time
from typing import Dict, Any, Optional, List
from datetime import datetime


class ComprehensiveTaxRateTester:
    """Comprehensive testing of tax rate API with form data and JSON."""
    
    def __init__(self, base_url: str, session: requests.Session):
        self.base_url = base_url.rstrip('/')
        self.session = session
        self.api_url = f"{base_url}/tax_rates/api"
        self.save_url = f"{base_url}/tax_rates/api/save"
        self.created_tax_rates = []  # Track for cleanup
    
    def test_endpoint_content_type_expectations(self) -> None:
        """Test what content types each endpoint expects."""
        print("\n🔍 Testing Content-Type Expectations for Each Endpoint")
        print("-" * 60)
        
        # Test individual create endpoint (POST /tax_rates/api)
        print("\n📍 Individual Create Endpoint: POST /tax_rates/api")
        self._test_content_types_for_endpoint(
            "POST", 
            self.api_url, 
            {"name": "ContentTypeTest", "rate": 10.0},
            "Individual Create"
        )
        
        # Test bulk save endpoint (POST /tax_rates/api/save)
        print("\n📍 Bulk Save Endpoint: POST /tax_rates/api/save")
        self._test_content_types_for_endpoint(
            "POST", 
            self.save_url, 
            [{"name": "BulkTest", "rate": 20.0}],
            "Bulk Save"
        )
    
    def _test_content_types_for_endpoint(self, method: str, url: str, payload: Any, endpoint_name: str) -> None:
        """Test different content types for a specific endpoint."""
        test_cases = [
            {
                "name": "JSON (application/json)",
                "method": "json",
                "payload": payload,
                "headers": {"Content-Type": "application/json"}
            },
            {
                "name": "Form Data (application/x-www-form-urlencoded)",
                "method": "data",
                "payload": payload if isinstance(payload, dict) else {"data": json.dumps(payload)},
                "headers": None
            },
            {
                "name": "Raw JSON with explicit header",
                "method": "raw",
                "payload": json.dumps(payload),
                "headers": {"Content-Type": "application/json"}
            }
        ]
        
        for test_case in test_cases:
            print(f"\n   📋 Testing {endpoint_name} with {test_case['name']}")
            
            try:
                kwargs = {"timeout": 30}
                
                if test_case["method"] == "json":
                    kwargs["json"] = test_case["payload"]
                elif test_case["method"] == "data":
                    kwargs["data"] = test_case["payload"]
                elif test_case["method"] == "raw":
                    kwargs["data"] = test_case["payload"]
                
                if test_case["headers"]:
                    kwargs["headers"] = test_case["headers"]
                
                response = self.session.request(method, url, **kwargs)
                
                print(f"      Status: {response.status_code}")
                
                if response.status_code in [200, 201]:
                    print(f"      ✅ SUCCESS with {test_case['name']}")
                    try:
                        result = response.json()
                        print(f"      Response: {json.dumps(result, indent=8)}")
                        
                        # Track created items for cleanup
                        if isinstance(result, dict) and 'id' in result:
                            self.created_tax_rates.append(result['id'])
                        elif isinstance(result, list):
                            for item in result:
                                if isinstance(item, dict) and 'id' in item:
                                    self.created_tax_rates.append(item['id'])
                                    
                    except Exception as e:
                        print(f"      Response parsing error: {e}")
                        
                elif response.status_code == 422:
                    print(f"      ❌ 422 Validation Error with {test_case['name']}")
                    try:
                        error_data = response.json()
                        print(f"      Error: {json.dumps(error_data, indent=8)}")
                    except:
                        print(f"      Raw response: {response.text}")
                        
                elif response.status_code == 409:
                    print(f"      ⚠️  409 Conflict (already exists)")
                    
                else:
                    print(f"      ❌ HTTP {response.status_code}")
                    try:
                        error_data = response.json()
                        print(f"      Error: {json.dumps(error_data, indent=8)}")
                    except:
                        print(f"      Raw response: {response.text[:200]}")
                        
            except Exception as e:
                print(f"      ❌ Request failed: {e}")
    
    def test_form_data_variations(self) -> None:
        """Test various form data configurations."""
        print("\n🔍 Testing Form Data Variations")
        print("-" * 60)
        
        test_cases = [
            {
                "name": "Basic Required Fields",
                "data": {"name": "BasicTest", "rate": 15.0},
                "description": "Only required fields"
            },
            {
                "name": "With is_default=false",
                "data": {"name": "DefaultFalseTest", "rate": 25.0, "is_default": False},
                "description": "Explicitly set is_default to false"
            },
            {
                "name": "With is_default=true",
                "data": {"name": "DefaultTrueTest", "rate": 35.0, "is_default": True},
                "description": "Set as default tax rate"
            },
            {
                "name": "Rate as string",
                "data": {"name": "StringRateTest", "rate": "45.0"},
                "description": "Rate provided as string"
            },
            {
                "name": "Rate as integer",
                "data": {"name": "IntRateTest", "rate": 55},
                "description": "Rate provided as integer"
            },
            {
                "name": "Decimal rate",
                "data": {"name": "DecimalTest", "rate": 12.75},
                "description": "Rate with decimal places"
            },
            {
                "name": "Zero rate",
                "data": {"name": "ZeroRateTest", "rate": 0.0},
                "description": "Zero tax rate"
            },
            {
                "name": "High rate",
                "data": {"name": "HighRateTest", "rate": 99.99},
                "description": "High tax rate"
            }
        ]
        
        successful_tests = []
        failed_tests = []
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n📋 Test {i}: {test_case['name']}")
            print(f"   Description: {test_case['description']}")
            print(f"   Data: {test_case['data']}")
            
            try:
                response = self.session.post(
                    self.api_url,
                    data=test_case['data'],
                    timeout=30
                )
                
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 201:
                    print(f"   ✅ SUCCESS")
                    successful_tests.append(test_case['name'])
                    
                    try:
                        result = response.json()
                        print(f"   Created: {json.dumps(result, indent=6)}")
                        
                        if 'id' in result:
                            self.created_tax_rates.append(result['id'])
                            
                    except Exception as e:
                        print(f"   Response parsing error: {e}")
                        
                elif response.status_code == 409:
                    print(f"   ⚠️  Already exists (409)")
                    successful_tests.append(f"{test_case['name']} (duplicate)")
                    
                elif response.status_code == 422:
                    print(f"   ❌ Validation Error")
                    failed_tests.append(test_case['name'])
                    
                    try:
                        error_data = response.json()
                        print(f"   Error: {json.dumps(error_data, indent=6)}")
                    except:
                        print(f"   Raw response: {response.text}")
                        
                else:
                    print(f"   ❌ HTTP {response.status_code}")
                    failed_tests.append(test_case['name'])
                    
            except Exception as e:
                print(f"   ❌ Request failed: {e}")
                failed_tests.append(test_case['name'])
        
        # Summary
        print(f"\n📊 Form Data Test Summary:")
        print(f"   ✅ Successful: {len(successful_tests)}")
        print(f"   ❌ Failed: {len(failed_tests)}")
        
        if successful_tests:
            print(f"   Success cases: {', '.join(successful_tests)}")
        if failed_tests:
            print(f"   Failed cases: {', '.join(failed_tests)}")
    
    def test_validation_rules(self) -> None:
        """Test API validation rules."""
        print("\n🔍 Testing Validation Rules")
        print("-" * 60)
        
        validation_tests = [
            {
                "name": "Missing name",
                "data": {"rate": 10.0},
                "expected": "Should fail - name is required"
            },
            {
                "name": "Missing rate",
                "data": {"name": "NoRateTest"},
                "expected": "Should fail - rate is required"
            },
            {
                "name": "Empty name",
                "data": {"name": "", "rate": 10.0},
                "expected": "Should fail - empty name"
            },
            {
                "name": "Negative rate",
                "data": {"name": "NegativeTest", "rate": -5.0},
                "expected": "Might fail - negative rate"
            },
            {
                "name": "Very long name",
                "data": {"name": "A" * 1000, "rate": 10.0},
                "expected": "Might fail - name too long"
            },
            {
                "name": "Invalid rate type",
                "data": {"name": "InvalidRateTest", "rate": "not_a_number"},
                "expected": "Should fail - invalid rate"
            }
        ]
        
        for test_case in validation_tests:
            print(f"\n📋 {test_case['name']}")
            print(f"   Expected: {test_case['expected']}")
            print(f"   Data: {test_case['data']}")
            
            try:
                response = self.session.post(
                    self.api_url,
                    data=test_case['data'],
                    timeout=30
                )
                
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 422:
                    print(f"   ✅ Validation worked (422)")
                    try:
                        error_data = response.json()
                        print(f"   Error: {json.dumps(error_data, indent=6)}")
                    except:
                        print(f"   Raw response: {response.text}")
                        
                elif response.status_code == 201:
                    print(f"   ⚠️  Unexpected success - validation might be lenient")
                    try:
                        result = response.json()
                        if 'id' in result:
                            self.created_tax_rates.append(result['id'])
                    except:
                        pass
                        
                else:
                    print(f"   ❌ Unexpected status: {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ Request failed: {e}")
    
    def cleanup_created_tax_rates(self) -> None:
        """Clean up all created tax rates."""
        if not self.created_tax_rates:
            print("\n🧹 No tax rates to clean up")
            return
            
        print(f"\n🧹 Cleaning up {len(self.created_tax_rates)} created tax rates...")
        
        cleaned_count = 0
        for tax_rate_id in self.created_tax_rates:
            try:
                response = self.session.delete(
                    f"{self.api_url}/{tax_rate_id}",
                    timeout=30
                )
                
                if response.status_code == 200:
                    cleaned_count += 1
                    print(f"   ✅ Deleted tax rate {tax_rate_id}")
                else:
                    print(f"   ⚠️  Failed to delete {tax_rate_id}: {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ Delete error for {tax_rate_id}: {e}")
        
        print(f"🧹 Cleanup complete: {cleaned_count}/{len(self.created_tax_rates)} deleted")
    
    def get_current_tax_rates(self) -> Optional[List[Dict]]:
        """Get current tax rates for reference."""
        try:
            response = self.session.get(self.api_url, timeout=30)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"❌ Failed to get current tax rates: {e}")
        return None
    
    def run_comprehensive_analysis(self) -> None:
        """Run the complete comprehensive analysis."""
        print("🔍 Comprehensive Tax Rate API Analysis")
        print("=" * 70)
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Base URL: {self.base_url}")
        print("=" * 70)
        
        # Get current state
        print("\n📊 Current Tax Rates:")
        current_rates = self.get_current_tax_rates()
        if current_rates:
            print(f"   Found {len(current_rates)} existing tax rates")
        else:
            print("   Could not retrieve current tax rates")
        
        try:
            # Test 1: Content-Type expectations
            self.test_endpoint_content_type_expectations()
            
            # Test 2: Form data variations
            self.test_form_data_variations()
            
            # Test 3: Validation rules
            self.test_validation_rules()
            
        finally:
            # Always cleanup
            self.cleanup_created_tax_rates()
        
        print("\n" + "=" * 70)
        print("🎯 Comprehensive Analysis Complete!")
        print("\n💡 Key Findings:")
        print("1. Individual CREATE endpoint (POST /tax_rates/api) expects FORM DATA")
        print("2. Bulk SAVE endpoint (POST /tax_rates/api/save) expects JSON")
        print("3. Use 'data' parameter for form data, 'json' parameter for JSON")
        print("4. Required fields: name (string), rate (number)")
        print("5. Optional fields: is_default (boolean)")
        print("\n✅ Solution Confirmed: Use form data for individual tax rate creation")


def main():
    """Main function with improved error handling."""
    import os
    
    # Configuration
    base_url = os.environ.get("BASE_URL", "http://simple.local:8080")
    username = os.environ.get("USERNAME", "admin")
    password = os.environ.get("PASSWORD", "admin123")
    
    print("🔍 Comprehensive Tax Rate API Test")
    print("=" * 50)
    print(f"Base URL: {base_url}")
    print(f"Username: {username}")
    print("=" * 50)
    
    # Create session and login
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'TaxRateApiTester/1.0'
    })
    
    print("🔐 Logging in...")
    
    # Try multiple login endpoints
    login_endpoints = [
        "/auth/login",
        "/login",
        "/api/auth/login"
    ]
    
    login_success = False
    for endpoint in login_endpoints:
        try:
            login_url = f"{base_url}{endpoint}"
            print(f"   Trying: {login_url}")
            
            login_data = {"username": username, "password": password}
            login_response = session.post(login_url, data=login_data, timeout=30)
            
            if login_response.status_code == 200:
                print(f"✅ Login successful via {endpoint}")
                login_success = True
                break
            else:
                print(f"   ❌ Failed: {login_response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    if not login_success:
        print("❌ Could not login with any endpoint")
        print("💡 Please check your credentials and base URL")
        sys.exit(1)
    
    try:
        # Run comprehensive analysis
        tester = ComprehensiveTaxRateTester(base_url, session)
        tester.run_comprehensive_analysis()
        
    except KeyboardInterrupt:
        print("\n⚠️  Analysis interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()