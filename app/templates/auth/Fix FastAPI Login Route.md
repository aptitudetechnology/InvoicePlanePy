# GitHub Copilot Instructions: Fix FastAPI Login Route

## Context
Your FastAPI app is returning 404 for `POST /login` requests. The logs show:
- `GET /auth/login` works (200 OK)
- `POST /login` fails (404 Not Found)

## Copilot Prompts to Use

### 1. Generate Missing POST Route
**Type this comment in your FastAPI file:**
```python
# Create POST route for /auth/login that handles form submission and redirects to dashboard on success
```

### 2. Fix Route Alignment
**Type this comment:**
```python
# Fix login routes - GET /auth/login shows form, POST /auth/login processes form data
```

### 3. Complete Login Handler
**Type this comment:**
```python
# Complete login function that validates credentials and creates session
```

## Specific Copilot Prompts

### For Route Definition
```python
# POST route for login form submission with username/password validation
@app.post("/auth/login")
async def login_user(request: Request, username: str = Form(...), password: str = Form(...)):
    # Let Copilot complete this function
```

### For Form Template Fix
```html
<!-- Form is already correct - action="/auth/login" matches the POST route -->
<form method="post" action="/auth/login">
    <!-- Demo credentials: admin/admin123 -->
```

### For Authentication Logic
```python
# Add authentication helper function that checks user credentials against database
def verify_user_credentials(username: str, password: str) -> bool:
    # Let Copilot generate the verification logic
```

## Expected Copilot Completions

### Route Handler
Copilot should suggest something like:
```python
@app.post("/auth/login")
async def login_user(request: Request, username: str = Form(...), password: str = Form(...)):
    # Demo credentials check
    if username == "admin" and password == "admin123":
        # Create session or JWT token
        return RedirectResponse(url="/dashboard", status_code=302)
    else:
        # Return to login with error
        return templates.TemplateResponse("login.html", {
            "request": request, 
            "error": "Invalid username or password"
        })
```

### Form Template
Copilot should suggest:
```html
<form method="post" action="/login">
    <input type="text" name="username" required>
    <input type="password" name="password" required>
    <button type="submit">Login</button>
</form>
```

## Tips for Better Copilot Results

1. **Be specific in comments** - mention FastAPI, forms, authentication
2. **Use consistent naming** - if you have `/auth/login` for GET, consider `/auth/login` for POST too
3. **Add context comments** about your database models (users table, etc.)
4. **Type function signatures first** - let Copilot fill in the body

## Quick Debug Steps

1. **Check your current routes:**
   ```python
   # Show all registered routes in FastAPI
   for route in app.routes:
       print(f"{route.methods} {route.path}")
   ```

2. **Verify form action matches route:**
   - Your form action is `/auth/login` ✅
   - You need a POST route for `/auth/login` ❌
   - Make sure you have both GET and POST for `/auth/login`

## Common Copilot Patterns for This Issue

Type these patterns and let Copilot complete:

```python
# Handle login form submission for /auth/login
@app.post("/auth/login")
async def process_login(

# Authenticate user with demo credentials admin/admin123
def authenticate_user(

# Login form template with error handling already exists
# Need to add POST route for /auth/login
```

The key is being specific about what you want Copilot to generate and providing enough context about your FastAPI application structure.