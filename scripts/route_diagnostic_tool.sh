#!/bin/bash

# Route Diagnostic Tool for Modal DOM Issues
# This script helps identify routing and path problems

echo "=============================================="
echo "ROUTE & PATH DIAGNOSTIC TOOL"
echo "=============================================="

# Function to find files recursively
find_files() {
    local pattern="$1"
    local description="$2"
    echo "=== $description ==="
    
    # Try different common locations
    find . -name "$pattern" -type f 2>/dev/null | head -10
    
    if [ $? -ne 0 ] || [ -z "$(find . -name "$pattern" -type f 2>/dev/null)" ]; then
        echo "⚠ No files found matching pattern: $pattern"
    fi
    echo ""
}

# Check current directory structure
echo "=== CURRENT DIRECTORY STRUCTURE ==="
pwd
echo "Contents:"
ls -la
echo ""

# Look for common web framework structures
echo "=== DETECTING FRAMEWORK STRUCTURE ==="
if [ -f "package.json" ]; then
    echo "✓ Node.js project detected"
    echo "Package.json contents:"
    head -20 package.json
elif [ -f "requirements.txt" ] || [ -f "app.py" ] || [ -f "manage.py" ]; then
    echo "✓ Python/Flask/Django project detected"
elif [ -f "composer.json" ] || [ -d "vendor" ]; then
    echo "✓ PHP project detected"
elif [ -f "Gemfile" ]; then
    echo "✓ Ruby project detected"
else
    echo "? Unknown or static project structure"
fi
echo ""

# Search for modal-related files
find_files "*.html" "HTML FILES"
find_files "*modal*" "MODAL-RELATED FILES"
find_files "*.js" "JAVASCRIPT FILES"
find_files "*.css" "CSS FILES"

# Look for template directories
echo "=== TEMPLATE DIRECTORY ANALYSIS ==="
common_template_dirs=("templates" "views" "public" "static" "assets" "src" "dist" "build")

for dir in "${common_template_dirs[@]}"; do
    if [ -d "$dir" ]; then
        echo "✓ Found: $dir/"
        find "$dir" -type f \( -name "*.html" -o -name "*.js" -o -name "*.css" \) | head -5
    fi
done
echo ""

# Check for route configuration files
echo "=== ROUTE CONFIGURATION FILES ==="
route_files=("routes.py" "urls.py" "routes.js" "app.js" "server.js" "web.php" "routes.php" ".htaccess" "config.ru")

for file in "${route_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✓ Found route file: $file"
        echo "First 10 lines:"
        head -10 "$file"
        echo "---"
    fi
done
echo ""

# Search for specific functions and IDs
echo "=== SEARCHING FOR MODAL-RELATED CODE ==="
echo "Searching for 'displayProductModal' function:"
grep -r "displayProductModal" . --include="*.js" --include="*.html" 2>/dev/null | head -5

echo ""
echo "Searching for 'productModal' ID:"
grep -r "productModal" . --include="*.js" --include="*.html" 2>/dev/null | head -5

echo ""
echo "Searching for modal-related classes:"
grep -r "modal" . --include="*.js" --include="*.html" --include="*.css" 2>/dev/null | head -10

echo ""

# Check file permissions
echo "=== FILE PERMISSIONS CHECK ==="
echo "Checking if files are accessible:"
if [ -f "index.html" ]; then
    ls -la index.html
fi

# Check for symbolic links
echo ""
echo "=== SYMBOLIC LINKS CHECK ==="
find . -type l 2>/dev/null | head -10

# Web server configuration check
echo ""
echo "=== WEB SERVER CONFIGURATION ==="
if [ -f ".htaccess" ]; then
    echo "✓ Apache .htaccess found:"
    cat .htaccess
elif [ -f "nginx.conf" ] || [ -f "nginx.config" ]; then
    echo "✓ Nginx config found"
elif [ -f "web.config" ]; then
    echo "✓ IIS web.config found"
fi

echo ""
echo "=== QUICK FIXES TO TRY ==="
echo "1. Check if your web server is serving from the correct directory"
echo "2. Verify file paths in your HTML includes/imports"
echo "3. Check for case sensitivity issues (productModal vs ProductModal)"
echo "4. Ensure JavaScript files are loaded before DOM manipulation"
echo "5. Check browser developer tools for 404 errors on resource loading"
echo ""

echo "=== RECOMMENDED NEXT STEPS ==="
echo "Run these commands to get more specific information:"
echo "  find . -name '*.html' -exec grep -l 'modal' {} \;"
echo "  find . -name '*.js' -exec grep -l 'productModal\\|displayProductModal' {} \;"
echo "  grep -r 'src=\\|href=' --include='*.html' . | grep -E '\\.js|\\.css'"
echo ""

echo "=============================================="
echo "DIAGNOSTIC COMPLETE"
echo "=============================================="