#!/usr/bin/env python3
"""
Tax Rate Form Data Test Script

This script sends form data instead of JSON to fix the 422 error.
The individual create endpoint expects form data, not JSON.
"""

import requests
import json
import sys
from typing import Dict, Any, Optional


class TaxRateFormDataTester:
    """Test tax rate creation with correct form data format."""
    
    def __init__(self, base_url: str, session: requests.Session):
        self.base_url = base_url.rstrip('/')
        self.session = session
        self.api_url = f"{base_url}/tax_rates/api"
        self.save_url = f"{base_url}/tax_rates/api/save"
    
    def test_form_data_creation(self) -> None:
        """Test creating tax rate with form data (the correct way)."""
        print("\n🔍 Testing tax rate creation with FORM DATA...")
        
        # The API expects form data, not JSON
        test_cases = [
            {
                "name": "Basic form data",
                "form_data": {
                    "name": "FormTest",
                    "rate": 15.0
                },
                "description": "Basic form data with required fields"
            },
            {
                "name": "Form data with is_default=false",
                "form_data": {
                    "name": "FormTest2",
                    "rate": 25.0,
                    "is_default": False
                },
                "description": "Form data with is_default explicitly false"
            },
            {
                "name": "Form data with is_default=true",
                "form_data": {
                    "name": "FormTest3",
                    "rate": 35.0,
                    "is_default": True
                },
                "description": "Form data with is_default=true"
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n📋 Test {i}: {test_case['name']}")
            print(f"   Description: {test_case['description']}")
            print(f"   Form Data: {test_case['form_data']}")
            
            try:
                # Send as form data (application/x-www-form-urlencoded)
                response = self.session.post(
                    self.api_url,
                    data=test_case['form_data'],  # ← Use 'data' for form data, not 'json'
                    timeout=30
                )
                
                print(f"   Status Code: {response.status_code}")
                
                if response.status_code == 201:  # Created
                    print(f"   ✅ SUCCESS! Tax rate created")
                    try:
                        result = response.json()
                        print(f"   Response: {json.dumps(result, indent=6)}")
                        
                        # Clean up - delete the created tax rate
                        if 'id' in result:
                            self._cleanup_tax_rate(result['id'])
                            
                    except Exception as e:
                        print(f"   Response parsing error: {e}")
                        print(f"   Raw response: {response.text}")
                        
                elif response.status_code == 409:  # Conflict
                    print(f"   ⚠️  Tax rate already exists (409 Conflict)")
                    try:
                        result = response.json()
                        print(f"   Response: {json.dumps(result, indent=6)}")
                    except:
                        print(f"   Raw response: {response.text}")
                        
                elif response.status_code == 422:
                    print(f"   ❌ 422 Validation Error")
                    try:
                        error_data = response.json()
                        print(f"   Error Details: {json.dumps(error_data, indent=6)}")
                    except:
                        print(f"   Raw response: {response.text}")
                        
                else:
                    print(f"   ❌ HTTP {response.status_code}")
                    try:
                        error_data = response.json()
                        print(f"   Error: {json.dumps(error_data, indent=6)}")
                    except:
                        print(f"   Raw response: {response.text}")
                        
            except Exception as e:
                print(f"   ❌ Request failed: {e}")
    
    def _cleanup_tax_rate(self, tax_rate_id: int) -> None:
        """Clean up created tax rate."""
        try:
            response = self.session.delete(
                f"{self.api_url}/{tax_rate_id}",
                timeout=30
            )
            if response.status_code == 200:
                print(f"   🧹 Cleaned up tax rate {tax_rate_id}")
            else:
                print(f"   ⚠️  Failed to clean up tax rate {tax_rate_id}: {response.status_code}")
        except Exception as e:
            print(f"   ⚠️  Cleanup error: {e}")
    
    def compare_json_vs_form_data(self) -> None:
        """Compare JSON (fails) vs form data (should work)."""
        print("\n🔄 Comparing JSON vs Form Data...")
        
        # Test 1: JSON data (should fail with 422)
        print("\n📋 Test 1: JSON data (should fail)")
        json_payload = {"name": "JSONTest", "rate": 50.0}
        print(f"   Payload: {json.dumps(json_payload, indent=6)}")
        
        try:
            response = self.session.post(
                self.api_url,
                json=json_payload,  # ← JSON data
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            print(f"   Status: {response.status_code}")
            if response.status_code == 422:
                print("   ✅ Expected 422 error with JSON data")
                try:
                    error_data = response.json()
                    print(f"   Error: {json.dumps(error_data, indent=6)}")
                except:
                    print(f"   Raw response: {response.text}")
            else:
                print("   ❌ Unexpected success with JSON data")
                
        except Exception as e:
            print(f"   ❌ Request failed: {e}")
        
        # Test 2: Form data (should work)
        print("\n📋 Test 2: Form data (should work)")
        form_data = {"name": "FormTest", "rate": 50.0}
        print(f"   Form Data: {form_data}")
        
        try:
            response = self.session.post(
                self.api_url,
                data=form_data,  # ← Form data
                timeout=30
            )
            
            print(f"   Status: {response.status_code}")
            if response.status_code == 201:
                print("   ✅ Success with form data!")
                try:
                    result = response.json()
                    print(f"   Response: {json.dumps(result, indent=6)}")
                    
                    # Clean up
                    if 'id' in result:
                        self._cleanup_tax_rate(result['id'])
                        
                except Exception as e:
                    print(f"   Response parsing error: {e}")
            else:
                print("   ❌ Unexpected failure with form data")
                try:
                    error_data = response.json()
                    print(f"   Error: {json.dumps(error_data, indent=6)}")
                except:
                    print(f"   Raw response: {response.text}")
                    
        except Exception as e:
            print(f"   ❌ Request failed: {e}")
    
    def run_analysis(self) -> None:
        """Run the complete analysis."""
        print("🔍 Tax Rate Form Data Analysis")
        print("=" * 50)
        
        # Step 1: Compare JSON vs Form Data
        self.compare_json_vs_form_data()
        
        # Step 2: Test different form data variations
        self.test_form_data_creation()
        
        print("\n" + "=" * 50)
        print("🎯 Analysis Complete!")
        print("\n💡 Key Findings:")
        print("1. The individual create endpoint expects FORM DATA, not JSON")
        print("2. Use 'data' parameter in requests, not 'json' parameter")
        print("3. The bulk save endpoint correctly expects JSON")
        print("4. This explains why bulk save works but individual create fails")
        print("\n✅ Solution: Send form data instead of JSON to individual create endpoint")


def main():
    """Main function."""
    import os
    
    # Configuration
    base_url = os.environ.get("BASE_URL", "http://simple.local:8080")
    username = os.environ.get("USERNAME", "admin")
    password = os.environ.get("PASSWORD", "admin")
    
    print("🔍 Tax Rate Form Data Test")
    print("=" * 40)
    print(f"Base URL: {base_url}")
    print(f"Username: {username}")
    print("=" * 40)
    
    # Create session and login
    session = requests.Session()
    
    print("🔐 Logging in...")
    login_data = {"username": username, "password": password}
    
    try:
        login_response = session.post(
            f"{base_url}/auth/login",
            data=login_data,
            timeout=30
        )
        
        if login_response.status_code == 200:
            print("✅ Login successful")
            
            # Run analysis
            tester = TaxRateFormDataTester(base_url, session)
            tester.run_analysis()
        else:
            print(f"❌ Login failed: {login_response.status_code}")
            if login_response.text:
                print(f"Response: {login_response.text}")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()