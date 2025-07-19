#!/bin/bash

# Modal DOM Element Test Script v2.0
# Enhanced debugging for JavaScript DOM element mismatch issues
# Now with auto-detection of template paths and comprehensive ID analysis

echo "=================================================="
echo "MODAL DOM ELEMENT MISMATCH TEST - VERSION 2.0"
echo "=================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Function to print section headers
print_header() {
    echo ""
    echo -e "${BLUE}=== $1 ===${NC}"
    echo ""
}

# Function to check file exists and report
check_file() {
    local file="$1"
    local description="$2"
    
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓ Found: $description${NC}"
        echo -e "  ${CYAN}Path: $file${NC}"
        return 0
    else
        echo -e "${RED}✗ Missing: $description${NC}"
        echo -e "  ${CYAN}Expected: $file${NC}"
        return 1
    fi
}

print_header "AUTO-DETECTING PROJECT STRUCTURE"

# Auto-detect template directories
TEMPLATE_DIRS=()
if [ -d "templates" ]; then
    TEMPLATE_DIRS+=("templates")
fi
if [ -d "app/templates" ]; then
    TEMPLATE_DIRS+=("app/templates")
fi
if [ -d "src/templates" ]; then
    TEMPLATE_DIRS+=("src/templates")
fi

echo "Detected template directories:"
for dir in "${TEMPLATE_DIRS[@]}"; do
    echo -e "  ${GREEN}• $dir${NC}"
done

# Find all HTML files that might contain the problematic JavaScript
print_header "LOCATING JAVASCRIPT FILES"

JS_FILES=()
while IFS= read -r -d '' file; do
    if grep -l "displayProductModal\|productList\.innerHTML" "$file" >/dev/null 2>&1; then
        JS_FILES+=("$file")
    fi
done < <(find . -name "*.html" -print0 2>/dev/null)

echo "Files containing problematic JavaScript:"
for file in "${JS_FILES[@]}"; do
    echo -e "  ${GREEN}• $file${NC}"
done

if [ ${#JS_FILES[@]} -eq 0 ]; then
    echo -e "${YELLOW}⚠ No JavaScript files found with displayProductModal function${NC}"
fi

# Find all potential modal files
print_header "LOCATING MODAL FILES"

MODAL_FILES=()
while IFS= read -r -d '' file; do
    if grep -l "productModal\|productList\|product.*modal" "$file" >/dev/null 2>&1; then
        MODAL_FILES+=("$file")
    fi
done < <(find . -name "*.html" -path "*/modal*" -o -name "*modal*.html" -print0 2>/dev/null)

echo "Potential modal files found:"
for file in "${MODAL_FILES[@]}"; do
    echo -e "  ${GREEN}• $file${NC}"
    
    # Quick preview of IDs in this file
    ids=$(grep -o 'id="[^"]*"' "$file" 2>/dev/null | sort -u | tr '\n' ' ')
    if [ -n "$ids" ]; then
        echo -e "    ${CYAN}IDs: $ids${NC}"
    fi
done

# Analyze the main JavaScript file for expected IDs
print_header "ANALYZING JAVASCRIPT EXPECTATIONS"

if [ ${#JS_FILES[@]} -gt 0 ]; then
    MAIN_JS_FILE="${JS_FILES[0]}"
    echo -e "Analyzing: ${CYAN}$MAIN_JS_FILE${NC}"
    echo ""
    
    # Extract all getElementById calls
    echo -e "${YELLOW}JavaScript expects these element IDs:${NC}"
    
    EXPECTED_IDS=()
    while IFS= read -r line; do
        id=$(echo "$line" | grep -o "getElementById(['\"][^'\"]*['\"])" | sed "s/getElementById(['\"]//g" | sed "s/['\"])//g")
        if [ -n "$id" ] && [[ "$id" == *"product"* ]]; then
            EXPECTED_IDS+=("$id")
            echo -e "  ${BLUE}→ '$id'${NC}"
        fi
    done < <(grep -n "getElementById" "$MAIN_JS_FILE" 2>/dev/null)
    
    # Extract querySelector calls
    echo ""
    echo -e "${YELLOW}JavaScript uses these selectors:${NC}"
    while IFS= read -r line; do
        selector=$(echo "$line" | grep -o "querySelector(['\"][^'\"]*['\"])" | sed "s/querySelector(['\"]//g" | sed "s/['\"])//g")
        if [ -n "$selector" ] && [[ "$selector" == *"product"* ]]; then
            echo -e "  ${PURPLE}→ '$selector'${NC}"
        fi
    done < <(grep -n "querySelector" "$MAIN_JS_FILE" 2>/dev/null)
    
    # Show the problematic line context
    echo ""
    echo -e "${YELLOW}Problematic code context (line ~985):${NC}"
    grep -n -A 3 -B 3 "productList\.innerHTML" "$MAIN_JS_FILE" 2>/dev/null | sed 's/^/  /' || echo "  Code not found"
    
else
    echo -e "${RED}No JavaScript files found to analyze${NC}"
fi

# Analyze modal files for actual IDs
print_header "ANALYZING MODAL HTML STRUCTURE"

ALL_MODAL_IDS=()
for modal_file in "${MODAL_FILES[@]}"; do
    echo -e "${CYAN}Analyzing: $modal_file${NC}"
    
    # Extract all IDs
    ids=$(grep -o 'id="[^"]*"' "$modal_file" 2>/dev/null | sed 's/id="//g' | sed 's/"//g')
    
    echo -e "${YELLOW}  Found IDs:${NC}"
    for id in $ids; do
        ALL_MODAL_IDS+=("$id")
        if [[ "$id" == *"product"* ]]; then
            echo -e "  ${GREEN}  ✓ $id${NC}"
        else
            echo -e "  ${CYAN}    $id${NC}"
        fi
    done
    
    # Extract classes that might be used instead of IDs
    echo -e "${YELLOW}  Found classes containing 'product':${NC}"
    classes=$(grep -o 'class="[^"]*product[^"]*"' "$modal_file" 2>/dev/null | sed 's/class="//g' | sed 's/"//g')
    for class in $classes; do
        echo -e "  ${PURPLE}    .$class${NC}"
    done
    
    echo ""
done

# Cross-reference expected vs actual IDs
print_header "MISMATCH ANALYSIS"

echo -e "${YELLOW}Cross-referencing JavaScript expectations with modal reality:${NC}"
echo ""

MISMATCHES=0
for expected_id in "${EXPECTED_IDS[@]}"; do
    found=false
    for modal_id in "${ALL_MODAL_IDS[@]}"; do
        if [ "$expected_id" = "$modal_id" ]; then
            found=true
            break
        fi
    done
    
    if [ "$found" = true ]; then
        echo -e "  ${GREEN}✓ '$expected_id' - FOUND${NC}"
    else
        echo -e "  ${RED}✗ '$expected_id' - MISSING${NC}"
        ((MISMATCHES++))
        
        # Suggest similar IDs
        echo -e "    ${YELLOW}Similar IDs found:${NC}"
        for modal_id in "${ALL_MODAL_IDS[@]}"; do
            if [[ "$modal_id" == *"${expected_id:0:7}"* ]] || [[ "$expected_id" == *"${modal_id:0:7}"* ]]; then
                echo -e "      ${CYAN}→ '$modal_id'${NC}"
            fi
        done
    fi
done

# Check for include statements
print_header "TEMPLATE INCLUDE ANALYSIS"

for js_file in "${JS_FILES[@]}"; do
    echo -e "${CYAN}Checking includes in: $js_file${NC}"
    
    includes=$(grep -n "{% include.*modal" "$js_file" 2>/dev/null)
    if [ -n "$includes" ]; then
        echo -e "${YELLOW}  Found include statements:${NC}"
        echo "$includes" | sed 's/^/    /'
        
        # Check if included files exist
        while IFS= read -r line; do
            include_path=$(echo "$line" | grep -o "{% include ['\"][^'\"]*['\"]" | sed "s/{% include ['\"]//g" | sed "s/['\"] %}//g" | sed "s/['\"].*//g")
            if [ -n "$include_path" ]; then
                full_path=""
                for template_dir in "${TEMPLATE_DIRS[@]}"; do
                    if [ -f "$template_dir/$include_path" ]; then
                        full_path="$template_dir/$include_path"
                        break
                    fi
                done
                
                if [ -n "$full_path" ]; then
                    echo -e "    ${GREEN}✓ Include file exists: $full_path${NC}"
                else
                    echo -e "    ${RED}✗ Include file missing: $include_path${NC}"
                    echo -e "      ${YELLOW}Searched in: ${TEMPLATE_DIRS[*]}${NC}"
                fi
            fi
        done <<< "$includes"
    else
        echo -e "${YELLOW}  No modal includes found${NC}"
    fi
done

# Final diagnosis and recommendations
print_header "DIAGNOSIS AND RECOMMENDATIONS"

if [ $MISMATCHES -eq 0 ] && [ ${#MODAL_FILES[@]} -gt 0 ]; then
    echo -e "${GREEN}✓ No ID mismatches detected!${NC}"
    echo -e "${YELLOW}The issue might be:${NC}"
    echo "  1. Modal file not being included properly"
    echo "  2. JavaScript running before DOM is ready"
    echo "  3. Modal being loaded dynamically"
    echo ""
    echo -e "${BLUE}Recommended debugging steps:${NC}"
    echo "  1. Add console.log to check if modal elements exist on page load"
    echo "  2. Verify the modal include path is correct"
    echo "  3. Check browser Network tab for 404 errors"
    
elif [ $MISMATCHES -gt 0 ]; then
    echo -e "${RED}✗ Found $MISMATCHES ID mismatches!${NC}"
    echo ""
    echo -e "${BLUE}RECOMMENDED FIXES:${NC}"
    
    # Generate specific fix recommendations
    for expected_id in "${EXPECTED_IDS[@]}"; do
        found=false
        for modal_id in "${ALL_MODAL_IDS[@]}"; do
            if [ "$expected_id" = "$modal_id" ]; then
                found=true
                break
            fi
        done
        
        if [ "$found" = false ]; then
            echo ""
            echo -e "${YELLOW}For missing ID '$expected_id':${NC}"
            echo "  Option 1: Add to your modal HTML:"
            echo "    <div id=\"$expected_id\">...</div>"
            echo ""
            echo "  Option 2: Update JavaScript to use existing ID:"
            
            # Find the most similar existing ID
            best_match=""
            best_score=0
            for modal_id in "${ALL_MODAL_IDS[@]}"; do
                # Simple similarity score based on common characters
                common_chars=$(echo "$expected_id$modal_id" | tr -d '\n' | fold -w1 | sort | uniq -d | wc -l)
                if [ $common_chars -gt $best_score ] && [[ "$modal_id" == *"product"* ]]; then
                    best_score=$common_chars
                    best_match="$modal_id"
                fi
            done
            
            if [ -n "$best_match" ]; then
                echo "    Change 'getElementById(\"$expected_id\")' to 'getElementById(\"$best_match\")'"
            fi
        fi
    done
    
else
    echo -e "${RED}✗ No modal files found!${NC}"
    echo ""
    echo -e "${BLUE}RECOMMENDED ACTIONS:${NC}"
    echo "  1. Create the missing modal file"
    echo "  2. Add it to your template includes"
    echo "  3. Ensure it has the required element IDs"
fi

print_header "QUICK FIX GENERATOR"

echo -e "${YELLOW}Quick JavaScript patch to handle missing elements:${NC}"
echo ""
echo "Add this to your JavaScript (temporary fix):"
echo ""
cat << 'EOF'
// Debug helper - add this to your DOMContentLoaded event
function debugModalElements() {
    console.log('=== MODAL DEBUG INFO ===');
    console.log('productModal exists:', !!document.getElementById('productModal'));
    console.log('productList exists:', !!document.getElementById('productList'));
    console.log('productSearch exists:', !!document.getElementById('productSearch'));
    
    console.log('All elements with "product" in ID:');
    document.querySelectorAll('[id*="product"]').forEach(el => {
        console.log(`  - ${el.tagName}#${el.id}`);
    });
    
    console.log('All elements with "product" in class:');
    document.querySelectorAll('[class*="product"]').forEach(el => {
        console.log(`  - ${el.tagName}.${el.className}`);
    });
}

// Call this in your DOMContentLoaded event
debugModalElements();
EOF

echo ""
echo -e "${GREEN}Script completed! Check the recommendations above.${NC}"
echo -e "${CYAN}TIP: Run this script again after making changes to verify fixes.${NC}"