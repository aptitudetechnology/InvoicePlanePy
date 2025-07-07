from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db, engine, Base
from app.routers import auth, dashboard, clients, invoices
from app.dependencies import get_current_user_optional
from app.models.user import User

# Import all models to ensure they're registered with Base
from app.models import user, client, invoice

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="InvoicePlane Python", version="1.0.0")

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Include routers
app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(clients.router)
app.include_router(invoices.router)

@app.get("/", response_class=HTMLResponse)
async def root(
    request: Request, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user_optional)
):
    if not current_user:
        return RedirectResponse(url="/login", status_code=302)
    
    # Redirect to dashboard
    return RedirectResponse(url="/dashboard", status_code=302)

@app.get("/health")
async def health_check():
    return {"status": "ok", "app": "InvoicePlane Python"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
