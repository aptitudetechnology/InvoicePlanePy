# Instructions: Create and Register Routes for `add_product_modal.html`

## 1. Create a Blueprint/Router for Product Modal

#**File:** `app/routers/product_modal.py`


from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from app.database import get_db
from app.models.product import Product
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

#@router.get("/modals/add_product_modal", response_class=HTMLResponse)
@router.get("/add_product_modal", response_class=HTMLResponse)
async def add_product_modal(request: Request, db: Session = Depends(get_db)):
    # Optionally fetch products from DB to pass to template
    products = db.query(Product).filter(Product.is_active == True).all()
    return templates.TemplateResponse("modals/add_product_modal.html", {
        "request": request,
        "products": products
    })
