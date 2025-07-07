from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.product import Product

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def products_list(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all products"""
    products = db.query(Product).all()
    
    return templates.TemplateResponse("products/list.html", {
        "request": request,
        "user": current_user,
        "products": products,
        "title": "Products"
    })

@router.get("/create", response_class=HTMLResponse)
async def create_product(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Show create product form"""
    return templates.TemplateResponse("products/create.html", {
        "request": request,
        "user": current_user,
        "title": "Create Product"
    })

@router.post("/create")
async def create_product_post(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Handle product creation"""
    # TODO: Implement product creation logic
    return RedirectResponse(url="/products", status_code=302)

@router.get("/{product_id}", response_class=HTMLResponse)
async def view_product(
    product_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """View a specific product"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return templates.TemplateResponse("products/view.html", {
        "request": request,
        "user": current_user,
        "product": product,
        "title": f"Product: {product.name}"
    })
