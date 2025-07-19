#!/bin/bash

# API Endpoint Test Script
# Tests various product endpoints to identify which ones exist and their response types

BASE_URL="http://simple.local:8080"
echo "Testing API endpoints for: $BASE_URL"
echo "=========================================="

# Function to test an endpoint
test_endpoint() {
    local endpoint="$1"
    local description="$2"
    local url="${BASE_URL}${endpoint}"
    
    echo ""
    echo "Testing: $description"
    echo "URL: $url"
    echo "----------------------------------------"
    
    # Test with curl, follow redirects, show status code
    response=$(curl -s -w "\nHTTP_STATUS:%{http_code}\nCONTENT_TYPE:%{content_type}\nRESPONSE_TIME:%{time_total}s\n" "$url")
    
    # Extract status code and content type
    status_code=$(echo "$response" | grep "HTTP_STATUS:" | cut -d: -f2)
    content_type=$(echo "$response" | grep "CONTENT_TYPE:" | cut -d: -f2)
    response_time=$(echo "$response" | grep "RESPONSE_TIME:" | cut -d: -f2)
    
    # Get response body (everything before the status lines)
    body=$(echo "$response" | sed '/HTTP_STATUS:/,$d')
    
    echo "Status: $status_code"
    echo "Content-Type: $content_type"
    echo "Response Time: $response_time"
    
    # Show first few lines of response
    if [ -n "$body" ]; then
        echo "Response preview:"
        echo "$body" | head -5
        if [ $(echo "$body" | wc -l) -gt 5 ]; then
            echo "... (truncated)"
        fi
    else
        echo "No response body"
    fi
    
    # Check if it looks like JSON
    if echo "$body" | jq . >/dev/null 2>&1; then
        echo "✅ Response appears to be valid JSON"
    elif [[ "$content_type" == *"json"* ]]; then
        echo "⚠️  Content-Type suggests JSON but body is not valid JSON"
    elif [[ "$content_type" == *"html"* ]]; then
        echo "📄 Response is HTML"
    fi
}

# Test the problematic endpoint
test_endpoint "/products/api" "Products API (the one failing)"

# Test existing endpoints from your route list
test_endpoint "/products/" "Products List"
test_endpoint "/products/families" "Product Families"
test_endpoint "/products/units" "Product Units"

# Test with AJAX-style headers to see if behavior changes
echo ""
echo ""
echo "Testing with AJAX headers (XMLHttpRequest):"
echo "=========================================="

test_ajax_endpoint() {
    local endpoint="$1"
    local description="$2"
    local url="${BASE_URL}${endpoint}"
    
    echo ""
    echo "Testing: $description (with AJAX headers)"
    echo "URL: $url"
    echo "----------------------------------------"
    
    response=$(curl -s -w "\nHTTP_STATUS:%{http_code}\nCONTENT_TYPE:%{content_type}\n" \
        -H "X-Requested-With: XMLHttpRequest" \
        -H "Accept: application/json, text/javascript, */*; q=0.01" \
        "$url")
    
    status_code=$(echo "$response" | grep "HTTP_STATUS:" | cut -d: -f2)
    content_type=$(echo "$response" | grep "CONTENT_TYPE:" | cut -d: -f2)
    body=$(echo "$response" | sed '/HTTP_STATUS:/,$d')
    
    echo "Status: $status_code"
    echo "Content-Type: $content_type"
    
    if [ -n "$body" ]; then
        echo "Response preview:"
        echo "$body" | head -3
    fi
    
    if echo "$body" | jq . >/dev/null 2>&1; then
        echo "✅ Response is valid JSON with AJAX headers"
    fi
}

test_ajax_endpoint "/products/" "Products List"
test_ajax_endpoint "/products/families" "Product Families"

echo ""
echo ""
echo "Summary:"
echo "========"
echo "Check the results above to see:"
echo "1. Which endpoint returns a 200 status code"
echo "2. Which endpoint returns JSON vs HTML"
echo "3. Whether AJAX headers change the response format"
echo ""
echo "This will help identify the correct endpoint to use in your JavaScript."