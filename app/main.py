from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
import os
from pathlib import Path

from app.database import get_db, engine, Base
from app.routers import auth, dashboard, clients, invoices, quotes, payments, products, tasks, reports, settings, help, notifications, profile, tax_rates
from app.dependencies import get_current_user_optional
from app.models.user import User

# Import all models to ensure they're registered with Base
from app.models import user, client, invoice, product, payment, api_key

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="InvoicePlane Python", version="1.0.0")

# Mount static files only if directory exists
static_dir = Path("static")
if static_dir.exists():
    app.mount("/static", StaticFiles(directory="static"), name="static")
else:
    # Create static directory structure for development
    static_dir.mkdir(exist_ok=True)
    (static_dir / "css").mkdir(exist_ok=True)
    (static_dir / "js").mkdir(exist_ok=True)
    (static_dir / "images").mkdir(exist_ok=True)
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
app.include_router(clients.router, prefix="/clients", tags=["clients"])
app.include_router(invoices.router, prefix="/invoices", tags=["invoices"])
app.include_router(quotes.router, prefix="/quotes", tags=["quotes"])
app.include_router(payments.router, prefix="/payments", tags=["payments"])
app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
app.include_router(reports.router, prefix="/reports", tags=["reports"])
app.include_router(settings.router, prefix="/settings", tags=["settings"])
app.include_router(help.router, prefix="/help", tags=["help"])
app.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
app.include_router(profile.router, prefix="/profile", tags=["profile"])
app.include_router(tax_rates.router, prefix="/settings/tax_rates", tags=["tax_rates"])

# Debug route to show all registered routes
@app.get("/debug/routes")
async def debug_routes():
    """Debug endpoint to show all registered routes"""
    routes = []
    for route in app.routes:
        if hasattr(route, 'methods') and hasattr(route, 'path'):
            routes.append({
                "path": route.path,
                "methods": list(route.methods),
                "name": getattr(route, 'name', None)
            })
    return {"routes": routes}

# Startup event to print routes when app starts
@app.on_event("startup")
async def startup_event():
    print("\n" + "="*50)
    print("🚀 FastAPI Routes Registered:")
    print("="*50)
    for route in app.routes:
        if hasattr(route, 'methods') and hasattr(route, 'path'):
            methods = ", ".join(route.methods)
            print(f"  {methods:<15} {route.path}")
    print("="*50 + "\n")
    
    # Check if login routes are properly configured
    check_login_routes()

def check_login_routes():
    """Check if login routes are properly configured"""
    auth_login_get = False
    auth_login_post = False
    
    for route in app.routes:
        if hasattr(route, 'methods') and hasattr(route, 'path'):
            if route.path == '/auth/login':
                if 'GET' in route.methods:
                    auth_login_get = True
                if 'POST' in route.methods:
                    auth_login_post = True
    
    print(f"✅ GET /auth/login exists: {auth_login_get}")
    print(f"{'✅' if auth_login_post else '❌'} POST /auth/login exists: {auth_login_post}")
    
    if not auth_login_post:
        print("\n❌ MISSING POST /auth/login ROUTE!")
        print("The authentication router may not be properly configured.")
        print("Check app/routers/auth.py for POST route definition.\n")

@app.get("/", response_class=HTMLResponse)
async def root(
    request: Request, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user_optional)
):
    if not current_user:
        return RedirectResponse(url="/auth/login", status_code=302)
    
    # Redirect to dashboard
    return RedirectResponse(url="/dashboard", status_code=302)

@app.get("/health")
async def health_check():
    return {"status": "ok", "app": "InvoicePlane Python"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
