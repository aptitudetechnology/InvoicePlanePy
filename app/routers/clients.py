from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from app.database import get_db
from app.models.user import User
from app.models.client import Client
from app.dependencies import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def clients_list(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    clients = db.query(Client).filter(Client.is_active == True).all()
    
    return templates.TemplateResponse(
        "clients/list.html", 
        {
            "request": request, 
            "user": current_user,
            "clients": clients
        }
    )

@router.get("/create", response_class=HTMLResponse)
async def client_create(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    return templates.TemplateResponse(
        "clients/create.html", 
        {"request": request, "user": current_user}
    )

@router.post("/", response_class=HTMLResponse)
async def client_create_post(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    # Personal Information
    is_active: bool = Form(False),
    name: str = Form(...),
    surname: Optional[str] = Form(None),
    language: str = Form("en"),
    # Address
    address_1: Optional[str] = Form(None),
    address_2: Optional[str] = Form(None),
    city: Optional[str] = Form(None),
    state: Optional[str] = Form(None),
    zip_code: Optional[str] = Form(None),
    country: Optional[str] = Form(None),
    # Contact Information
    phone: Optional[str] = Form(None),
    fax: Optional[str] = Form(None),
    mobile: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    website: Optional[str] = Form(None),
    # Personal Information (Additional)
    gender: Optional[str] = Form(None),
    birthdate: Optional[str] = Form(None),
    company: Optional[str] = Form(None),
    # Taxes Information
    vat_id: Optional[str] = Form(None),
    tax_code: Optional[str] = Form(None),
    abn: Optional[str] = Form(None),
    # Notes
    notes: Optional[str] = Form(None)
):
    """Create a new client"""
    try:
        # Parse birthdate if provided
        parsed_birthdate = None
        if birthdate:
            try:
                parsed_birthdate = datetime.strptime(birthdate, "%Y-%m-%d").date()
            except ValueError:
                parsed_birthdate = None
        
        # Create new client
        client = Client(
            # Personal Information
            is_active=is_active,
            name=name.strip(),
            surname=surname.strip() if surname else None,
            language=language,
            # Address
            address_1=address_1.strip() if address_1 else None,
            address_2=address_2.strip() if address_2 else None,
            city=city.strip() if city else None,
            state=state.strip() if state else None,
            zip_code=zip_code.strip() if zip_code else None,
            country=country,
            # Contact Information
            phone=phone.strip() if phone else None,
            fax=fax.strip() if fax else None,
            mobile=mobile.strip() if mobile else None,
            email=email.strip() if email else None,
            website=website.strip() if website else None,
            # Personal Information (Additional)
            gender=gender,
            birthdate=parsed_birthdate,
            company=company.strip() if company else None,
            # Taxes Information
            vat_id=vat_id.strip() if vat_id else None,
            tax_code=tax_code.strip() if tax_code else None,
            abn=abn.strip() if abn else None,
            # Notes
            notes=notes.strip() if notes else None
        )
        
        db.add(client)
        db.commit()
        db.refresh(client)
        
        # Redirect to client list with success message
        return RedirectResponse(url="/clients", status_code=302)
        
    except Exception as e:
        db.rollback()
        # In a real application, you'd want to show this error to the user
        # For now, we'll just redirect back to the form
        return RedirectResponse(url="/clients/create", status_code=302)

@router.get("/{client_id}", response_class=HTMLResponse)
async def client_view(
    client_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """View a specific client"""
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        return RedirectResponse(url="/clients", status_code=302)
    
    return templates.TemplateResponse(
        "clients/view.html", 
        {
            "request": request, 
            "user": current_user,
            "client": client
        }
    )

@router.get("/{client_id}/edit", response_class=HTMLResponse)
async def client_edit(
    client_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Edit a specific client"""
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        return RedirectResponse(url="/clients", status_code=302)
    
    return templates.TemplateResponse(
        "clients/edit.html", 
        {
            "request": request, 
            "user": current_user,
            "client": client
        }
    )
