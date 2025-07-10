# app/routers/tax_rates.py
from fastapi import APIRouter, Depends, Request, Form, HTTPException, status, Body
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.user import User
from app.models.tax_rate import TaxRate
from app.dependencies import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# --- BULK SAVE ENDPOINT ---
@router.post("/tax_rates/api/save", response_class=JSONResponse)
async def bulk_save_tax_rates(
    payload: dict = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Bulk save endpoint for tax rates. Accepts a list of tax rates and updates/inserts/deletes as needed.
    Expects JSON: { "tax_rates": [ {id, name, rate}, ... ] }
    """
    tax_rates_in = payload.get("tax_rates", [])
    if not isinstance(tax_rates_in, list):
        raise HTTPException(status_code=400, detail="tax_rates must be a list")

    # Fetch all existing tax rates from DB
    db_tax_rates = db.query(TaxRate).all()
    db_tax_rates_by_id = {tr.id: tr for tr in db_tax_rates}
    incoming_ids = set()

    # Update or create
    for tr_in in tax_rates_in:
        tr_id = tr_in.get("id")
        name = tr_in.get("name", "").strip()
        rate = tr_in.get("rate")
        if not name or rate is None or not (0 <= rate <= 100):
            continue  # skip invalid
        if tr_id and tr_id in db_tax_rates_by_id:
            # Update existing
            tr = db_tax_rates_by_id[tr_id]
            tr.name = name
            tr.rate = rate
            db.add(tr)
            incoming_ids.add(tr_id)
        else:
            # Create new
            new_tr = TaxRate(name=name, rate=rate)
            db.add(new_tr)
            db.flush()  # assign id
            incoming_ids.add(new_tr.id)

    # Delete tax rates not present in incoming list
    for tr in db_tax_rates:
        if tr.id not in incoming_ids:
            db.delete(tr)

    db.commit()

    return {"message": "Tax rates saved successfully!"}

# --- HTML Page Route ---

@router.get("/tax_rates", response_class=HTMLResponse)
async def tax_rates_page(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Renders the tax rates configuration page.
    Fetches all tax rates to pre-populate the table on page load.
    """
    tax_rates = db.query(TaxRate).order_by(TaxRate.name).all()
    
    # Convert SQLAlchemy objects to a list of dictionaries for easier JSON serialization
    # This is useful if you later decide to use this directly in JSON response,
    # or to pass a clean data structure to the template (though not strictly necessary for Jinja2)
    tax_rates_data = [
        {"id": tr.id, "name": tr.name, "rate": tr.rate, "is_default": tr.is_default}
        for tr in tax_rates
    ]

    return templates.TemplateResponse(
        "settings/tax_rates.html", # Assuming your template is at app/templates/settings/tax_rates.html
        {
            "request": request, 
            "user": current_user,
            "tax_rates_initial_data": tax_rates_data # Pass initial data to the frontend
        }
    )

# --- API Endpoints for AJAX Calls ---

@router.get("/tax_rates/api", response_class=JSONResponse)
async def get_all_tax_rates_api(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # Ensure user is authenticated for API access
):
    """
    API endpoint to get all tax rates.
    """
    tax_rates = db.query(TaxRate).order_by(TaxRate.name).all()
    tax_rates_data = [
        {"id": tr.id, "name": tr.name, "rate": tr.rate, "is_default": tr.is_default}
        for tr in tax_rates
    ]
    return JSONResponse(content=tax_rates_data)


@router.post("/tax_rates/api", response_class=JSONResponse)
async def create_tax_rate_api(
    name: str = Form(...),
    rate: float = Form(...),
    is_default: Optional[bool] = Form(False), # Added is_default form field
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    API endpoint to create a new tax rate.
    """
    # Basic validation (FastAPI Form(...) handles required, but you can add more)
    if not (0 <= rate <= 100):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tax rate must be between 0 and 100."
        )
    
    # Check if a tax rate with the same name already exists
    existing_tax_rate = db.query(TaxRate).filter(TaxRate.name == name.strip()).first()
    if existing_tax_rate:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, # 409 Conflict indicates a resource conflict
            detail=f"Tax rate with name '{name.strip()}' already exists."
        )

    # Handle `is_default` logic: ensure only one tax rate can be default
    if is_default:
        current_default = db.query(TaxRate).filter(TaxRate.is_default == True).first()
        if current_default:
            current_default.is_default = False
            db.add(current_default) # Mark current default as not default

    new_tax_rate = TaxRate(name=name.strip(), rate=rate, is_default=is_default)
    
    db.add(new_tax_rate)
    db.commit()
    db.refresh(new_tax_rate)

    return JSONResponse(
        content={
            "id": new_tax_rate.id,
            "name": new_tax_rate.name,
            "rate": new_tax_rate.rate,
            "is_default": new_tax_rate.is_default,
            "message": "Tax rate created successfully!"
        },
        status_code=status.HTTP_201_CREATED
    )


@router.put("/tax_rates/api/{tax_rate_id}", response_class=JSONResponse)
async def update_tax_rate_api(
    tax_rate_id: int,
    name: str = Form(...),
    rate: float = Form(...),
    is_default: Optional[bool] = Form(False),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    API endpoint to update an existing tax rate.
    """
    tax_rate = db.query(TaxRate).filter(TaxRate.id == tax_rate_id).first()
    if not tax_rate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tax rate not found."
        )

    # Basic validation
    if not (0 <= rate <= 100):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tax rate must be between 0 and 100."
        )

    # Check for name conflict if the name is being changed
    if tax_rate.name != name.strip():
        existing_tax_rate = db.query(TaxRate).filter(TaxRate.name == name.strip()).first()
        if existing_tax_rate and existing_tax_rate.id != tax_rate_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Tax rate with name '{name.strip()}' already exists."
            )
            
    # Handle `is_default` logic: ensure only one tax rate can be default
    if is_default and not tax_rate.is_default: # If setting this one as default and it wasn't before
        current_default = db.query(TaxRate).filter(TaxRate.is_default == True).first()
        if current_default and current_default.id != tax_rate_id:
            current_default.is_default = False
            db.add(current_default)
    elif tax_rate.is_default and not is_default: # If unsetting this one as default
        # If this was the only default, you might want to prevent unsetting it
        # or prompt the user to select a new default. For now, we'll allow unsetting.
        pass
    
    tax_rate.name = name.strip()
    tax_rate.rate = rate
    tax_rate.is_default = is_default # Update the default status

    db.add(tax_rate) # Add to session for update, though usually not strictly necessary after query.first()
    db.commit()
    db.refresh(tax_rate)

    return JSONResponse(
        content={
            "id": tax_rate.id,
            "name": tax_rate.name,
            "rate": tax_rate.rate,
            "is_default": tax_rate.is_default,
            "message": "Tax rate updated successfully!"
        }
    )


@router.delete("/tax_rates/api/{tax_rate_id}", response_class=JSONResponse)
async def delete_tax_rate_api(
    tax_rate_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    API endpoint to delete a tax rate.
    """
    tax_rate = db.query(TaxRate).filter(TaxRate.id == tax_rate_id).first()
    if not tax_rate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tax rate not found."
        )
    
    if tax_rate.is_default:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete the default tax rate. Please set another tax rate as default first."
        )

    db.delete(tax_rate)
    db.commit()

    return JSONResponse(
        content={"message": "Tax rate deleted successfully!"},
        status_code=status.HTTP_200_OK
    )