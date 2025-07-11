#!/usr/bin/env python3
"""
Tax Rate API Test Script

This script tests the persistence and functionality of a tax rate API.
It performs comprehensive tests including data persistence, error handling,
and cleanup operations.
"""

import requests
import os
import sys
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class TaxRate:
    """Represents a tax rate entry."""
    name: str
    rate: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {"name": self.name, "rate": self.rate}


class TaxRateAPITester:
    """Handles tax rate API testing operations."""
    
    def __init__(self, timeout: int = 10):
        self.base_url = os.environ.get("TAX_RATE_BASE_URL", "http://localhost:8000")
        self.api_url = f"{self.base_url}/tax_rates/api"
        self.save_url = f"{self.base_url}/tax_rates/api/save"
        self.timeout = timeout
        self.test_tax_rate = TaxRate("DebugTest", 42.0)
        
    def _make_request(self, method: str, url: str, **kwargs) -> Optional[requests.Response]:
        """Make HTTP request with error handling and timeout."""
        try:
            kwargs.setdefault('timeout', self.timeout)
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.Timeout:
            print(f"❌ Request timed out after {self.timeout} seconds")
            return None
        except requests.exceptions.ConnectionError:
            print(f"❌ Connection error: Could not connect to {url}")
            return None
        except requests.exceptions.HTTPError as e:
            print(f"❌ HTTP error: {e}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Request error: {e}")
            return None
    
    def fetch_tax_rates(self) -> Optional[List[Dict[str, Any]]]:
        """Fetch current tax rates from API."""
        print("📋 Fetching current tax rates from API...")
        
        response = self._make_request('GET', self.api_url)
        if not response:
            return None
            
        try:
            data = response.json()
            if isinstance(data, list):
                print(f"✅ Found {len(data)} tax rates")
                for rate in data:
                    if isinstance(rate, dict) and 'name' in rate and 'rate' in rate:
                        print(f"   - {rate['name']}: {rate['rate']}%")
                return data
            else:
                print(f"⚠️  Unexpected data format: {type(data)}")
                return None
        except ValueError as e:
            print(f"❌ Invalid JSON response: {e}")
            return None
    
    def save_tax_rates(self, tax_rates: List[Dict[str, Any]]) -> bool:
        """Save tax rates to API."""
        print(f"💾 Saving {len(tax_rates)} tax rates...")
        
        payload = {"tax_rates": tax_rates}
        response = self._make_request('POST', self.save_url, json=payload)
        
        if response:
            print(f"✅ Save successful: {response.status_code}")
            return True
        else:
            print("❌ Save failed")
            return False
    
    def create_tax_rate(self, tax_rate: TaxRate) -> Optional[Dict[str, Any]]:
        """Create a single tax rate using the POST API."""
        print(f"➕ Creating tax rate: {tax_rate.name} ({tax_rate.rate}%)")
        
        response = self._make_request('POST', self.api_url, json=tax_rate.to_dict())
        if response:
            try:
                created_rate = response.json()
                print(f"✅ Tax rate created successfully")
                return created_rate
            except ValueError as e:
                print(f"❌ Invalid JSON response: {e}")
                return None
        else:
            print("❌ Failed to create tax rate")
            return None
    
    def delete_tax_rate(self, tax_rate_id: int) -> bool:
        """Delete a tax rate by ID."""
        print(f"🗑️  Deleting tax rate with ID: {tax_rate_id}")
        
        delete_url = f"{self.api_url}/{tax_rate_id}"
        response = self._make_request('DELETE', delete_url)
        
        if response:
            print(f"✅ Delete successful: {response.status_code}")
            return True
        else:
            print("❌ Delete failed")
            return False
    
    def validate_tax_rate_exists(self, tax_rates: List[Dict[str, Any]], target_rate: TaxRate) -> bool:
        """Check if a specific tax rate exists in the list."""
        for rate in tax_rates:
            if (rate.get("name") == target_rate.name and 
                rate.get("rate") == target_rate.rate):
                return True
        return False
    
    def find_tax_rate_by_name(self, tax_rates: List[Dict[str, Any]], name: str) -> Optional[Dict[str, Any]]:
        """Find a tax rate by name."""
        for rate in tax_rates:
            if rate.get("name") == name:
                return rate
        return None
    
    def check_database_configuration(self) -> None:
        """Check database configuration for persistence warnings."""
        print("\n🔍 Checking database configuration...")
        
        database_url = os.environ.get("DATABASE_URL")
        if database_url:
            print(f"📊 DATABASE_URL: {database_url}")
            if ":memory:" in database_url.lower():
                print("⚠️  WARNING: Using in-memory database - data will not persist between restarts!")
            else:
                print("✅ Database appears to be persistent")
        else:
            print("⚠️  DATABASE_URL not set - check your application configuration")
        
        # Check other common database environment variables
        db_vars = ["DB_HOST", "DB_NAME", "DB_USER", "POSTGRES_URL", "SQLITE_DB"]
        found_vars = {var: os.environ.get(var) for var in db_vars if os.environ.get(var)}
        
        if found_vars:
            print("📋 Other database-related environment variables:")
            for var, value in found_vars.items():
                # Mask sensitive information
                if any(keyword in var.lower() for keyword in ['password', 'secret', 'key']):
                    value = "***masked***"
                print(f"   - {var}: {value}")
    
    def test_crud_operations(self) -> bool:
        """Test Create, Read, Update, Delete operations."""
        print("\n🧪 Testing CRUD operations...")
        
        # Step 1: Create a new tax rate
        created_rate = self.create_tax_rate(self.test_tax_rate)
        if not created_rate:
            print("❌ Failed to create tax rate - aborting CRUD test")
            return False
        
        # Extract ID from created rate
        tax_rate_id = created_rate.get('id')
        if not tax_rate_id:
            print("❌ No ID returned from created tax rate")
            return False
        
        # Step 2: Verify creation by fetching all rates
        print("\n🔍 Verifying creation...")
        time.sleep(1)  # Brief pause to ensure data is committed
        
        current_rates = self.fetch_tax_rates()
        if current_rates is None:
            print("❌ Could not fetch tax rates after creation")
            return False
        
        test_exists = self.validate_tax_rate_exists(current_rates, self.test_tax_rate)
        if test_exists:
            print("✅ CREATE test PASSED - tax rate found")
        else:
            print("❌ CREATE test FAILED - tax rate not found")
            return False
        
        # Step 3: Cleanup - Delete the test rate
        print("\n🧹 Cleaning up test data...")
        if self.delete_tax_rate(tax_rate_id):
            print("✅ DELETE test PASSED")
            
            # Verify deletion
            final_rates = self.fetch_tax_rates()
            if final_rates and not self.validate_tax_rate_exists(final_rates, self.test_tax_rate):
                print("✅ Delete verification passed")
            else:
                print("⚠️  Delete verification failed - test data may still exist")
        else:
            print("❌ DELETE test FAILED")
        
        return test_exists
    
    def test_bulk_save_workflow(self) -> bool:
        """Test the bulk save persistence workflow."""
        print("\n🧪 Testing bulk save workflow...")
        
        # Step 1: Fetch original tax rates
        original_rates = self.fetch_tax_rates()
        if original_rates is None:
            print("❌ Could not fetch original tax rates - aborting test")
            return False
        
        # Step 2: Add test tax rate
        print(f"\n➕ Adding test tax rate to bulk save: {self.test_tax_rate.name} ({self.test_tax_rate.rate}%)")
        updated_rates = original_rates + [self.test_tax_rate.to_dict()]
        
        if not self.save_tax_rates(updated_rates):
            print("❌ Failed to save updated tax rates")
            return False
        
        # Step 3: Verify persistence
        print("\n🔍 Verifying bulk save persistence...")
        time.sleep(1)  # Brief pause to ensure data is committed
        
        current_rates = self.fetch_tax_rates()
        if current_rates is None:
            print("❌ Could not fetch tax rates after bulk save")
            return False
        
        test_exists = self.validate_tax_rate_exists(current_rates, self.test_tax_rate)
        if test_exists:
            print("✅ Bulk save persistence test PASSED - test tax rate found")
        else:
            print("❌ Bulk save persistence test FAILED - test tax rate not found")
        
        # Step 4: Cleanup
        print("\n🧹 Cleaning up bulk save test data...")
        cleaned_rates = [rate for rate in current_rates 
                        if rate.get("name") != self.test_tax_rate.name]
        
        if self.save_tax_rates(cleaned_rates):
            print("✅ Bulk save cleanup successful")
            
            # Verify cleanup
            final_rates = self.fetch_tax_rates()
            if final_rates and not self.validate_tax_rate_exists(final_rates, self.test_tax_rate):
                print("✅ Bulk save cleanup verification passed")
            else:
                print("⚠️  Bulk save cleanup verification failed - test data may still exist")
        else:
            print("❌ Bulk save cleanup failed - test data may persist")
        
        return test_exists
    
    def run_connectivity_test(self) -> bool:
        """Test basic API connectivity."""
        print("\n🌐 Testing API connectivity...")
        
        # Test GET endpoint
        print(f"Testing GET: {self.api_url}")
        get_response = self._make_request('GET', self.api_url)
        get_success = get_response is not None
        
        if get_success:
            print("✅ GET endpoint accessible")
        else:
            print("❌ GET endpoint failed")
        
        return get_success
    
    def run_all_tests(self) -> bool:
        """Run all tests and return overall success."""
        print("🚀 Starting Tax Rate API Tests")
        print("=" * 50)
        
        # Configuration check
        self.check_database_configuration()
        
        # Connectivity test
        if not self.run_connectivity_test():
            print("\n❌ Connectivity test failed - aborting remaining tests")
            return False
        
        # CRUD operations test
        crud_success = self.test_crud_operations()
        
        # Bulk save test
        bulk_save_success = self.test_bulk_save_workflow()
        
        # Summary
        print("\n" + "=" * 50)
        overall_success = crud_success and bulk_save_success
        
        if overall_success:
            print("🎉 All tests PASSED!")
        else:
            print("❌ Some tests FAILED!")
            print(f"   - CRUD operations: {'✅ PASSED' if crud_success else '❌ FAILED'}")
            print(f"   - Bulk save: {'✅ PASSED' if bulk_save_success else '❌ FAILED'}")
        
        return overall_success


def main():
    """Main entry point."""
    # Configuration
    timeout = int(os.environ.get("API_TIMEOUT", "10"))
    
    print("Tax Rate API Test Script")
    print(f"Timeout: {timeout} seconds")
    print("-" * 30)
    
    # Run tests
    tester = TaxRateAPITester(timeout=timeout)
    success = tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()