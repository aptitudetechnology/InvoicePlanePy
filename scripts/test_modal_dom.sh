#!/bin/bash

# Modal DOM Element Test Script
# Tests the theory that JavaScript is looking for wrong element IDs

echo "==================================="
echo "MODAL DOM ELEMENT MISMATCH TEST"
echo "==================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Testing theory: JavaScript looks for wrong element IDs${NC}"
echo ""

# Define the expected vs actual element IDs
echo -e "${YELLOW}EXPECTED by JavaScript:${NC}"
echo "- document.getElementById('productList')"
echo "- document.getElementById('productSearch')"
echo "- document.getElementById('productModal')"
echo ""

echo -e "${YELLOW}ACTUAL in Modal HTML:${NC}"
echo ""

# Check if modal file exists
MODAL_FILE="templates/modals/add_product_modal.html"
if [ -f "$MODAL_FILE" ]; then
    echo -e "${GREEN}✓ Modal file exists: $MODAL_FILE${NC}"
    echo ""
    
    # Search for specific IDs in the modal file
    echo -e "${BLUE}Searching for element IDs in modal file:${NC}"
    echo ""
    
    # Check for productModal
    if grep -q 'id="productModal"' "$MODAL_FILE"; then
        echo -e "${GREEN}✓ Found: id=\"productModal\"${NC}"
    else
        echo -e "${RED}✗ Missing: id=\"productModal\"${NC}"
    fi
    
    # Check for productList (expected by JS)
    if grep -q 'id="productList"' "$MODAL_FILE"; then
        echo -e "${GREEN}✓ Found: id=\"productList\"${NC}"
    else
        echo -e "${RED}✗ Missing: id=\"productList\"${NC}"
        # Check for alternative IDs
        if grep -q 'id="productTableBody"' "$MODAL_FILE"; then
            echo -e "${YELLOW}  → Found instead: id=\"productTableBody\"${NC}"
        fi
    fi
    
    # Check for productSearch (expected by JS)
    if grep -q 'id="productSearch"' "$MODAL_FILE"; then
        echo -e "${GREEN}✓ Found: id=\"productSearch\"${NC}"
    else
        echo -e "${RED}✗ Missing: id=\"productSearch\"${NC}"
        # Check for alternative search IDs
        if grep -q 'id="productNameSearch"' "$MODAL_FILE"; then
            echo -e "${YELLOW}  → Found instead: id=\"productNameSearch\"${NC}"
        fi
    fi
    
    echo ""
    echo -e "${BLUE}All IDs found in modal file:${NC}"
    grep -n 'id="[^"]*"' "$MODAL_FILE" | sed 's/^/  /'
    
else
    echo -e "${RED}✗ Modal file NOT found: $MODAL_FILE${NC}"
    echo ""
    echo "Checking if modal directory exists..."
    if [ -d "templates/modals" ]; then
        echo -e "${YELLOW}→ Directory exists: templates/modals/${NC}"
        echo "Files in modals directory:"
        ls -la templates/modals/ | sed 's/^/  /'
    else
        echo -e "${RED}✗ Directory missing: templates/modals/${NC}"
    fi
fi

echo ""
echo -e "${BLUE}Checking main template for JavaScript functions:${NC}"
echo ""

# Look for the problematic JavaScript functions
MAIN_TEMPLATE="templates/quotes/edit.html"  # Adjust path as needed
if [ -f "$MAIN_TEMPLATE" ]; then
    echo -e "${GREEN}✓ Found main template: $MAIN_TEMPLATE${NC}"
    
    # Check for displayProductModal function
    if grep -q "function displayProductModal" "$MAIN_TEMPLATE"; then
        echo -e "${GREEN}✓ Found: displayProductModal() function${NC}"
        
        # Extract the problematic line (around line 985)
        echo ""
        echo -e "${YELLOW}Problematic code in displayProductModal():${NC}"
        grep -A 5 -B 5 "productList\.innerHTML" "$MAIN_TEMPLATE" | sed 's/^/  /'
    else
        echo -e "${RED}✗ Missing: displayProductModal() function${NC}"
    fi
    
else
    # Try to find any HTML file with the JavaScript
    echo "Searching for main template with JavaScript..."
    FOUND_FILE=$(find . -name "*.html" -exec grep -l "displayProductModal" {} \; | head -1)
    if [ -n "$FOUND_FILE" ]; then
        echo -e "${GREEN}✓ Found JavaScript in: $FOUND_FILE${NC}"
        
        echo ""
        echo -e "${YELLOW}Problematic code in displayProductModal():${NC}"
        grep -A 5 -B 5 "productList\.innerHTML" "$FOUND_FILE" | sed 's/^/  /'
    else
        echo -e "${RED}✗ Could not find JavaScript file${NC}"
    fi
fi

echo ""
echo "==================================="
echo -e "${BLUE}DIAGNOSIS:${NC}"
echo "==================================="

if [ -f "$MODAL_FILE" ]; then
    # Check if the mismatch exists
    HAS_PRODUCT_LIST=$(grep -c 'id="productList"' "$MODAL_FILE")
    HAS_PRODUCT_SEARCH=$(grep -c 'id="productSearch"' "$MODAL_FILE")
    HAS_TABLE_BODY=$(grep -c 'id="productTableBody"' "$MODAL_FILE")
    HAS_NAME_SEARCH=$(grep -c 'id="productNameSearch"' "$MODAL_FILE")
    
    if [ "$HAS_PRODUCT_LIST" -eq 0 ] && [ "$HAS_TABLE_BODY" -gt 0 ]; then
        echo -e "${RED}CONFIRMED: ID mismatch detected!${NC}"
        echo "- JavaScript expects: id='productList'"
        echo "- Modal actually has: id='productTableBody'"
        echo ""
    fi
    
    if [ "$HAS_PRODUCT_SEARCH" -eq 0 ] && [ "$HAS_NAME_SEARCH" -gt 0 ]; then
        echo -e "${RED}CONFIRMED: Search ID mismatch detected!${NC}"
        echo "- JavaScript expects: id='productSearch'"
        echo "- Modal actually has: id='productNameSearch'"
        echo ""
    fi
    
    if [ "$HAS_PRODUCT_LIST" -eq 0 ] || [ "$HAS_PRODUCT_SEARCH" -eq 0 ]; then
        echo -e "${YELLOW}RECOMMENDATION:${NC}"
        echo "Update your JavaScript to use the correct IDs:"
        echo "- Change 'productList' to 'productTableBody'"
        echo "- Change 'productSearch' to 'productNameSearch'"
        echo ""
        echo "OR update your modal HTML to use the expected IDs."
    else
        echo -e "${GREEN}No ID mismatch found - issue may be elsewhere${NC}"
    fi
else
    echo -e "${RED}CONFIRMED: Modal file missing!${NC}"
    echo "The template tries to include 'modals/add_product_modal.html' but it doesn't exist."
fi

echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "1. Fix the ID mismatches identified above"
echo "2. Test the modal functionality"
echo "3. Check browser console for any remaining errors"
echo ""
echo "Script completed!"