from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def profile_page(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Show user profile page"""
    return templates.TemplateResponse("profile/index.html", {
        "request": request,
        "user": current_user,
        "title": "User Profile"
    })

@router.get("/edit", response_class=HTMLResponse)
async def edit_profile(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Show edit profile form"""
    return templates.TemplateResponse("profile/edit.html", {
        "request": request,
        "user": current_user,
        "title": "Edit Profile"
    })

@router.post("/edit")
async def update_profile(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    # Account Information
    first_name: str = Form(...),
    last_name: str = Form(...),
    company: Optional[str] = Form(None),
    email: str = Form(...),
    language: str = Form(default="en"),
    user_type: str = Form(default="user"),
    # Address Information
    street_address: Optional[str] = Form(None),
    street_address_2: Optional[str] = Form(None),
    city: Optional[str] = Form(None),
    state: Optional[str] = Form(None),
    zip_code: Optional[str] = Form(None),
    country: Optional[str] = Form(None),
    # Tax Information
    vat_id: Optional[str] = Form(None),
    tax_code: Optional[str] = Form(None),
    iban: Optional[str] = Form(None),
    acn: Optional[str] = Form(None),
    abn: Optional[str] = Form(None),
    subscriber_number: Optional[str] = Form(None),
    # Contact Information
    phone_number: Optional[str] = Form(None),
    fax_number: Optional[str] = Form(None),
    mobile_number: Optional[str] = Form(None),
    web_address: Optional[str] = Form(None)
):
    """Update user profile"""
    try:
        # Update basic fields
        current_user.first_name = first_name
        current_user.last_name = last_name
        current_user.email = email
        current_user.company = company
        current_user.language = language
        current_user.role = user_type
        
        # Update address fields
        current_user.street_address = street_address
        current_user.street_address_2 = street_address_2
        current_user.city = city
        current_user.state = state
        current_user.zip_code = zip_code
        current_user.country = country
        
        # Update tax fields
        current_user.vat_id = vat_id
        current_user.tax_code = tax_code
        current_user.iban = iban
        current_user.acn = acn
        current_user.abn = abn
        current_user.subscriber_number = subscriber_number
        
        # Update contact fields
        current_user.phone_number = phone_number
        current_user.fax_number = fax_number
        current_user.mobile_number = mobile_number
        current_user.web_address = web_address
        
        db.commit()
        
        return RedirectResponse(url="/profile?updated=1", status_code=302)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Failed to update profile")

@router.get("/account", response_class=HTMLResponse)
async def account_settings(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Show account settings page"""
    return templates.TemplateResponse("profile/account.html", {
        "request": request,
        "user": current_user,
        "title": "Account Settings"
    })

@router.get("/security", response_class=HTMLResponse)
async def security_settings(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Show security settings page"""
    return templates.TemplateResponse("profile/security.html", {
        "request": request,
        "user": current_user,
        "title": "Security Settings"
    })
