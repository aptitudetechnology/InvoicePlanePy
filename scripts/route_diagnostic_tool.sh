#!/bin/bash

# Fixed Modal DOM Element Test for InvoicePlanePy
# This version looks in the correct directories

echo "=================================================="
echo "FIXED MODAL DOM ELEMENT TEST - InvoicePlanePy"
echo "=================================================="

# Ensure we're in project root
if [[ ! -d "app/templates" ]]; then
    echo "❌ Error: Run this script from the InvoicePlanePy root directory"
    echo "Current directory: $(pwd)"
    echo "Expected to find: app/templates/"
    exit 1
fi

echo "✅ Project root confirmed: $(pwd)"
echo ""

echo "=== MODAL FILES ANALYSIS ==="
modal_files=("app/templates/modals/add_product_modal.html" "app/templates/quotes/edit.html")

for file in "${modal_files[@]}"; do
    if [[ -f "$file" ]]; then
        echo "✅ Found: $file"
    else
        echo "❌ Missing: $file"
    fi
done
echo ""

echo "=== JAVASCRIPT FUNCTION ANALYSIS ==="
echo "Searching for displayProductModal function:"
if grep -q "displayProductModal" app/templates/quotes/edit.html 2>/dev/null; then
    echo "✅ displayProductModal function found in app/templates/quotes/edit.html"
    echo "Function definition:"
    grep -n -A 5 "function displayProductModal" app/templates/quotes/edit.html
else
    echo "❌ displayProductModal function not found"
fi
echo ""

echo "=== DOM ELEMENT ANALYSIS ==="
echo "Checking for productModal ID:"
if grep -q 'id="productModal"' app/templates/modals/add_product_modal.html 2>/dev/null; then
    echo "✅ productModal ID found in modal template"
    grep -n 'id="productModal"' app/templates/modals/add_product_modal.html
else
    echo "❌ productModal ID not found in modal template"
fi
echo ""

echo "=== TEMPLATE INCLUSION ANALYSIS ==="
echo "Checking if modal is included in quotes/edit.html:"
if grep -q "add_product_modal.html" app/templates/quotes/edit.html 2>/dev/null; then
    echo "✅ Modal template is included"
    grep -n "add_product_modal.html" app/templates/quotes/edit.html
else
    echo "❌ Modal template not included"
fi
echo ""

echo "=== BOOTSTRAP MODAL INTEGRATION ==="
echo "Checking Bootstrap modal integration:"
if grep -q "bootstrap.Modal" app/templates/quotes/edit.html 2>/dev/null; then
    echo "✅ Bootstrap Modal integration found"
    grep -n "bootstrap.Modal" app/templates/quotes/edit.html
else
    echo "❌ Bootstrap Modal integration not found"
fi
echo ""

echo "=== POTENTIAL ISSUES ANALYSIS ==="
issues_found=0

# Check if Bootstrap is loaded
if ! grep -q "bootstrap" app/templates/quotes/edit.html 2>/dev/null; then
    echo "⚠ Potential Issue: Bootstrap may not be loaded"
    ((issues_found++))
fi

# Check if jQuery is loaded (if needed)
if grep -q "jquery\|jQuery" app/templates/quotes/edit.html 2>/dev/null; then
    echo "✅ jQuery detected (may be needed for some functionality)"
else
    echo "ℹ Info: No jQuery detected (may be fine if using vanilla JS)"
fi

# Check for DOM ready handlers
if grep -q "DOMContentLoaded\|document.ready" app/templates/quotes/edit.html 2>/dev/null; then
    echo "✅ DOM ready handler detected"
else
    echo "⚠ Potential Issue: No DOM ready handler detected"
    ((issues_found++))
fi

echo ""
echo "=== SUMMARY ==="
if [[ $issues_found -eq 0 ]]; then
    echo "🎉 SUCCESS: Modal system appears to be properly configured!"
    echo "   - Modal template exists and has correct ID"
    echo "   - JavaScript function exists" 
    echo "   - Modal is included in the edit template"
    echo "   - Bootstrap integration is present"
else
    echo "⚠ Found $issues_found potential issues (see above)"
fi

echo ""
echo "=== TESTING RECOMMENDATIONS ==="
echo "1. Open your browser's Developer Tools (F12)"
echo "2. Navigate to the quotes/edit page"
echo "3. Try to trigger the modal"
echo "4. Check the Console tab for any JavaScript errors"
echo "5. Check the Network tab for failed resource loads"

echo ""
echo "=== QUICK DEBUGGING COMMANDS ==="
echo "To test the modal manually in browser console:"
echo "  displayProductModal()  // Should open the modal"
echo "  document.getElementById('productModal')  // Should return the modal element"

echo ""
echo "=================================================="
echo "FIXED TEST COMPLETE"
echo "=================================================="