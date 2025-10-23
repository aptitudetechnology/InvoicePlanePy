from fastapi import APIRouter, Request, Depends, HTTPException, Form, Query
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_, asc, desc
import logging

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.product import Product, ProductFamily, ProductUnit
from app.models.tax_rate import TaxRate
# from app.auth import get_current_admin_user  # Adjust import based on your auth structure

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Add the new API endpoint
@router.get("/api")
async def get_products_api(
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_user),  # Temporarily removed for testing
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(100, ge=1, le=1000, description="Items per page"),
    search: str = Query(None, description="Search products by name or SKU"),
    family_id: int = Query(None, description="Filter by product family ID"),
    sort_by: str = Query("name", description="Sort by: name, price, created_at, sku"),
    sort_order: str = Query("asc", description="Sort order: asc or desc")
):
    """
    Get paginated list of products for the admin interface.
    Includes related family and unit information.
    """
    try:
        offset = (page - 1) * limit
        
        # Base query with eager loading of related data
        products_query = db.query(Product).join(
            ProductFamily, Product.family_id == ProductFamily.id, isouter=True
        ).join(
            ProductUnit, Product.unit_id == ProductUnit.id, isouter=True
        ).join(
            TaxRate, Product.tax_rate_id == TaxRate.id, isouter=True
        )
        
        # Apply search filter if provided
        if search:
            search_term = f"%{search}%"
            products_query = products_query.filter(
                or_(
                    Product.name.ilike(search_term),
                    Product.sku.ilike(search_term),
                    Product.description.ilike(search_term)
                )
            )
        
        # Apply family filter if provided
        if family_id:
            products_query = products_query.filter(Product.family_id == family_id)
        
        # Apply sorting
        sort_column = None
        if sort_by == "name":
            sort_column = Product.name
        elif sort_by == "price":
            sort_column = Product.price
        elif sort_by == "sku":
            sort_column = Product.sku
        elif sort_by == "created_at":
            # Assuming you have a created_at field, adjust if different
            sort_column = getattr(Product, 'created_at', Product.id)
        else:
            sort_column = Product.name  # Default fallback
        
        if sort_order.lower() == "desc":
            products_query = products_query.order_by(desc(sort_column))
        else:
            products_query = products_query.order_by(asc(sort_column))
        
        # Get paginated results
        products = products_query.offset(offset).limit(limit).all()
        
        # Get total count for pagination
        total_query = db.query(Product)
        if search:
            search_term = f"%{search}%"
            total_query = total_query.filter(
                or_(
                    Product.name.ilike(search_term),
                    Product.sku.ilike(search_term),
                    Product.description.ilike(search_term)
                )
            )
        if family_id:
            total_query = total_query.filter(Product.family_id == family_id)
        total_products = total_query.count()
        
        # Format products data with related information
        products_data = []
        for product in products:
            # Get related family and unit data
            family_data = None
            if product.family:
                family_data = {
                    "id": product.family.id,
                    "name": product.family.name
                }
            
            unit_data = None
            if product.unit:
                unit_data = {
                    "id": product.unit.id,
                    "name": product.unit.name,
                    "abbreviation": product.unit.abbreviation
                }
            
            product_data = {
                "id": product.id,
                "name": product.name,
                "sku": product.sku,
                "price": float(product.price) if product.price is not None else None,
                "description": product.description if product.description else None,
                "family": family_data,
                "unit": unit_data,
                # Additional fields from your model
                "tax_rate": {
                    "id": product.tax_rate_rel.id if product.tax_rate_rel else None,
                    "name": product.tax_rate_rel.name if product.tax_rate_rel else None,
                    "rate": float(product.tax_rate_rel.rate) if product.tax_rate_rel else None
                } if product.tax_rate_rel else None,
                "provider_name": product.provider_name,
                "purchase_price": float(product.purchase_price) if product.purchase_price is not None else None,
                "sumex": product.sumex,
                "tariff": float(product.tariff) if product.tariff is not None else None,
                "user_id": product.user_id,
                # Add created_at if it exists in your model
                "created_at": product.created_at.isoformat() if hasattr(product, 'created_at') and product.created_at else None,
                # Add is_active field if it exists, otherwise assume active
                "is_active": getattr(product, 'is_active', True)
            }
            products_data.append(product_data)
        
        return {
            "products": products_data,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total_products,
                "total_pages": (total_products + limit - 1) // limit
            },
            "filters": {
                "search": search,
                "sort_by": sort_by,
                "sort_order": sort_order
            }
        }
        
    except SQLAlchemyError as e:
        logging.error(f"Database error in get_products_api: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logging.error(f"Unexpected error in get_products_api: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@router.get("/api/families")
async def get_families_api(
    db: Session = Depends(get_db)
    # Temporarily removed authentication for testing
    # current_user: User = Depends(get_current_user)
):
    """
    Get all active product families for the product modal.
    """
    try:
        families = db.query(ProductFamily).filter(ProductFamily.is_active == True).order_by(ProductFamily.name).all()
        
        families_data = []
        for family in families:
            families_data.append({
                "id": family.id,
                "name": family.name
            })
        
        return {"families": families_data}
        
    except SQLAlchemyError as e:
        logging.error(f"Database error in get_families_api: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logging.error(f"Unexpected error in get_families_api: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

# Existing endpoints continue below...

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
    family_id: str = Form(""),
    unit_id: str = Form(""),
    tax_rate_id: str = Form(""),
    purchase_price: str = Form(""),
    provider_name: str = Form(""),
    sumex: str = Form(None),
    tariff: str = Form(""),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Handle product creation"""
    product = Product(
        name=name,
        description=description if description else None,
        price=price,
        sku=sku if sku else None,
        family_id=int(family_id) if family_id else None,
        unit_id=int(unit_id) if unit_id else None,
        tax_rate_id=int(tax_rate_id) if tax_rate_id else None,
        purchase_price=float(purchase_price) if purchase_price else None,
        provider_name=provider_name if provider_name else None,
        sumex=sumex == "true",
        tariff=float(tariff) if tariff else None,
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
    product = db.query(Product).options(
        joinedload(Product.family),
        joinedload(Product.unit),
        joinedload(Product.tax_rate_rel)
    ).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return templates.TemplateResponse("products/view.html", {
        "request": request,
        "user": current_user,
        "product": product,
        "title": f"Product: {product.name}"
    })

@router.get("/{product_id}/edit", response_class=HTMLResponse)
async def edit_product(
    product_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Edit a specific product"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    families = db.query(ProductFamily).filter(ProductFamily.is_active == True).all()
    units = db.query(ProductUnit).filter(ProductUnit.is_active == True).all()
    tax_rates = db.query(TaxRate).filter(TaxRate.is_default == True).all()
    
    return templates.TemplateResponse("products/edit.html", {
        "request": request,
        "user": current_user,
        "product": product,
        "families": families,
        "units": units,
        "tax_rates": tax_rates,
        "title": f"Edit Product: {product.name}"
    })

@router.post("/{product_id}/edit")
async def update_product(
    product_id: int,
    request: Request,
    name: str = Form(...),
    description: str = Form(""),
    price: float = Form(...),
    sku: str = Form(""),
    family_id: str = Form(""),
    unit_id: str = Form(""),
    tax_rate_id: str = Form(""),
    provider_name: str = Form(""),
    purchase_price: str = Form(""),
    sumex: str = Form(None),
    tariff: str = Form(""),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Handle product update"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.name = name
    product.description = description if description else None
    product.price = price
    product.sku = sku if sku else None
    product.family_id = int(family_id) if family_id else None
    product.unit_id = int(unit_id) if unit_id else None
    product.tax_rate_id = int(tax_rate_id) if tax_rate_id else None
    product.provider_name = provider_name if provider_name else None
    product.purchase_price = float(purchase_price) if purchase_price else None
    # Convert sumex checkbox to boolean
    product.sumex = sumex == "true"
    product.tariff = float(tariff) if tariff else None

    db.commit()

    return RedirectResponse(url=f"/products/{product_id}", status_code=302)

@router.get("/families/{family_id}", response_class=HTMLResponse)
async def view_product_family(
    family_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """View a specific product family"""
    family = db.query(ProductFamily).filter(ProductFamily.id == family_id).first()
    if not family:
        return templates.TemplateResponse("errors/not_found.html", {
            "request": request,
            "message": f"Product family with ID {family_id} not found."
        }, status_code=404)
    
    return templates.TemplateResponse("products/family_view.html", {
        "request": request,
        "user": current_user,
        "family": family,
        "title": f"Product Family: {family.name}"
    })

@router.get("/families/{family_id}/edit", response_class=HTMLResponse)
async def edit_product_family(
    family_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Edit a specific product family"""
    family = db.query(ProductFamily).filter(ProductFamily.id == family_id).first()
    if not family:
        return templates.TemplateResponse("errors/not_found.html", {
            "request": request,
            "message": f"Product family with ID {family_id} not found."
        }, status_code=404)
    
    return templates.TemplateResponse("products/family_edit.html", {
        "request": request,
        "user": current_user,
        "family": family,
        "title": f"Edit Product Family: {family.name}"
    })

@router.get("/units/{unit_id}", response_class=HTMLResponse)
async def view_product_unit(
    unit_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """View a specific product unit"""
    unit = db.query(ProductUnit).filter(ProductUnit.id == unit_id).first()
    if not unit:
        return templates.TemplateResponse("errors/not_found.html", {
            "request": request,
            "message": f"Product unit with ID {unit_id} not found."
        }, status_code=404)
    
    return templates.TemplateResponse("products/unit_view.html", {
        "request": request,
        "user": current_user,
        "unit": unit,
        "title": f"Product Unit: {unit.name}"
    })

@router.get("/units/{unit_id}/edit", response_class=HTMLResponse)
async def edit_product_unit(
    unit_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Edit a specific product unit"""
    unit = db.query(ProductUnit).filter(ProductUnit.id == unit_id).first()
    if not unit:
        return templates.TemplateResponse("errors/not_found.html", {
            "request": request,
            "message": f"Product unit with ID {unit_id} not found."
        }, status_code=404)
    
    return templates.TemplateResponse("products/unit_edit.html", {
        "request": request,
        "user": current_user,
        "unit": unit,
        "title": f"Edit Product Unit: {unit.name}"
    })