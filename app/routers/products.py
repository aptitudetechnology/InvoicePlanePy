from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.product import Product, ProductFamily, ProductUnit

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
        "title": "View Products"
    })

@router.get("/create", response_class=HTMLResponse)
async def create_product(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Show create product form"""
    families = db.query(ProductFamily).filter(ProductFamily.is_active == True).all()
    units = db.query(ProductUnit).filter(ProductUnit.is_active == True).all()
    
    return templates.TemplateResponse("products/create.html", {
        "request": request,
        "user": current_user,
        "families": families,
        "units": units,
        "title": "Create Product"
    })

@router.post("/create")
async def create_product_post(
    request: Request,
    name: str = Form(...),
    description: str = Form(""),
    price: float = Form(...),
    sku: str = Form(""),
    family_id: int = Form(None),
    unit_id: int = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Handle product creation"""
    product = Product(
        name=name,
        description=description,
        price=price,
        sku=sku if sku else None,
        family_id=family_id if family_id else None,
        unit_id=unit_id if unit_id else None,
        user_id=current_user.id
    )
    
    db.add(product)
    db.commit()
    
    return RedirectResponse(url="/products", status_code=302)

@router.get("/families", response_class=HTMLResponse)
async def product_families(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """View product families"""
    families = db.query(ProductFamily).all()
    
    return templates.TemplateResponse("products/families.html", {
        "request": request,
        "user": current_user,
        "families": families,
        "title": "View Product Families"
    })

@router.get("/families/create", response_class=HTMLResponse)
async def create_product_family(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Show create product family form"""
    return templates.TemplateResponse("products/create_family.html", {
        "request": request,
        "user": current_user,
        "title": "Create Product Family"
    })

@router.post("/families/create")
async def create_product_family_post(
    request: Request,
    name: str = Form(...),
    description: str = Form(""),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Handle product family creation"""
    family = ProductFamily(
        name=name,
        description=description
    )
    
    db.add(family)
    db.commit()
    
    return RedirectResponse(url="/products/families", status_code=302)

@router.get("/units", response_class=HTMLResponse)
async def product_units(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """View product units"""
    units = db.query(ProductUnit).all()
    
    return templates.TemplateResponse("products/units.html", {
        "request": request,
        "user": current_user,
        "units": units,
        "title": "View Product Units"
    })

@router.get("/units/create", response_class=HTMLResponse)
async def create_product_unit(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Show create product unit form"""
    return templates.TemplateResponse("products/create_unit.html", {
        "request": request,
        "user": current_user,
        "title": "Create Product Unit"
    })

@router.post("/units/create")
async def create_product_unit_post(
    request: Request,
    name: str = Form(...),
    abbreviation: str = Form(...),
    description: str = Form(""),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Handle product unit creation"""
    unit = ProductUnit(
        name=name,
        abbreviation=abbreviation,
        description=description
    )
    
    db.add(unit)
    db.commit()
    
    return RedirectResponse(url="/products/units", status_code=302)

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
