from fastapi import APIRouter, Depends, Request, Form, HTTPException, Query
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc
from datetime import datetime
from typing import Optional
import logging

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

@router.get("/api")
async def get_clients_api(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(100, ge=1, le=1000, description="Items per page"),
    search: str = Query(None, description="Search clients by name, email, company, or phone"),
    is_active: bool = Query(True, description="Filter by active status"),
    sort_by: str = Query("name", description="Sort by: name, email, company, created_at"),
    sort_order: str = Query("asc", description="Sort order: asc or desc")
):
    """
    Get paginated list of clients with full contact information.
    Returns JSON data for API integration.
    """
    try:
        offset = (page - 1) * limit

        # Base query
        clients_query = db.query(Client)

        # Apply active filter (default to active clients only)
        clients_query = clients_query.filter(Client.is_active == is_active)

        # Apply user filter (non-admin users only see their own clients if applicable)
        # Note: Clients don't have a direct user relationship in this schema,
        # but we can add this later if needed for multi-tenant scenarios

        # Apply search filter if provided
        if search:
            search_term = f"%{search}%"
            clients_query = clients_query.filter(
                or_(
                    Client.name.ilike(search_term),
                    Client.surname.ilike(search_term),
                    Client.email.ilike(search_term),
                    Client.company.ilike(search_term),
                    Client.phone.ilike(search_term),
                    Client.mobile.ilike(search_term)
                )
            )

        # Apply sorting
        sort_column = None
        if sort_by == "name":
            sort_column = Client.name
        elif sort_by == "email":
            sort_column = Client.email
        elif sort_by == "company":
            sort_column = Client.company
        elif sort_by == "created_at":
            sort_column = Client.created_at
        else:
            sort_column = Client.name  # Default fallback

        if sort_order.lower() == "desc":
            clients_query = clients_query.order_by(desc(sort_column))
        else:
            clients_query = clients_query.order_by(asc(sort_column))

        # Get paginated results
        clients = clients_query.offset(offset).limit(limit).all()

        # Get total count for pagination
        total_query = db.query(Client).filter(Client.is_active == is_active)
        if search:
            search_term = f"%{search}%"
            total_query = total_query.filter(
                or_(
                    Client.name.ilike(search_term),
                    Client.surname.ilike(search_term),
                    Client.email.ilike(search_term),
                    Client.company.ilike(search_term),
                    Client.phone.ilike(search_term),
                    Client.mobile.ilike(search_term)
                )
            )
        total_clients = total_query.count()

        # Format clients data
        clients_data = []
        for client in clients:
            client_data = {
                "id": client.id,
                "is_active": client.is_active,
                "name": client.name,
                "surname": client.surname,
                "company": client.company,
                "email": client.email,
                "phone": client.phone,
                "fax": client.fax,
                "mobile": client.mobile,
                "website": client.website,
                "address_1": client.address_1,
                "address_2": client.address_2,
                "city": client.city,
                "state": client.state,
                "zip_code": client.zip_code,
                "country": client.country,
                "language": client.language,
                "gender": client.gender,
                "birthdate": str(client.birthdate) if client.birthdate else None,
                "vat_id": client.vat_id,
                "tax_code": client.tax_code,
                "abn": client.abn,
                "title": client.title,
                "notes": client.notes,
                "created_at": client.created_at.isoformat() if hasattr(client, 'created_at') and client.created_at else None,
                "updated_at": client.updated_at.isoformat() if hasattr(client, 'updated_at') and client.updated_at else None
            }
            clients_data.append(client_data)

        return {
            "clients": clients_data,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total_clients,
                "total_pages": (total_clients + limit - 1) // limit
            },
            "filters": {
                "search": search,
                "is_active": is_active,
                "sort_by": sort_by,
                "sort_order": sort_order
            }
        }

    except Exception as e:
        logging.error(f"Unexpected error in get_clients_api: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


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


@router.get("/{client_id}/api", response_class=JSONResponse)
async def get_client_api(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get a specific client with full contact information.
    Returns JSON data for API integration.
    """
    try:
        client = db.query(Client).filter(Client.id == client_id).first()

        if not client:
            raise HTTPException(status_code=404, detail="Client not found")

        # Check if client is active (unless admin)
        if not client.is_active and not current_user.is_admin:
            raise HTTPException(status_code=404, detail="Client not found")

        # Format client data
        client_data = {
            "id": client.id,
            "is_active": client.is_active,
            "name": client.name,
            "surname": client.surname,
            "company": client.company,
            "email": client.email,
            "phone": client.phone,
            "fax": client.fax,
            "mobile": client.mobile,
            "website": client.website,
            "address_1": client.address_1,
            "address_2": client.address_2,
            "city": client.city,
            "state": client.state,
            "zip_code": client.zip_code,
            "country": client.country,
            "language": client.language,
            "gender": client.gender,
            "birthdate": str(client.birthdate) if client.birthdate else None,
            "vat_id": client.vat_id,
            "tax_code": client.tax_code,
            "abn": client.abn,
            "title": client.title,
            "notes": client.notes,
            "created_at": client.created_at.isoformat() if hasattr(client, 'created_at') and client.created_at else None,
            "updated_at": client.updated_at.isoformat() if hasattr(client, 'updated_at') and client.updated_at else None
        }

        return client_data

    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Unexpected error in get_client_api: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
