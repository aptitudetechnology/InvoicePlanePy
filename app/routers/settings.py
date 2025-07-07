from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def settings_page(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Show settings page"""
    return templates.TemplateResponse("settings/index.html", {
        "request": request,
        "user": current_user,
        "title": "Settings"
    })

@router.get("/company", response_class=HTMLResponse)
async def company_settings(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Show company settings"""
    return templates.TemplateResponse("settings/company.html", {
        "request": request,
        "user": current_user,
        "title": "Company Settings"
    })

@router.get("/users", response_class=HTMLResponse)
async def user_settings(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Show user management"""
    users = db.query(User).all()
    return templates.TemplateResponse("settings/users.html", {
        "request": request,
        "user": current_user,
        "users": users,
        "title": "User Management"
    })

@router.get("/invoice", response_class=HTMLResponse)
async def invoice_settings(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Show invoice settings"""
    return templates.TemplateResponse("settings/invoice.html", {
        "request": request,
        "user": current_user,
        "title": "Invoice Settings"
    })

@router.get("/custom-fields", response_class=HTMLResponse)
async def custom_fields(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Show custom fields management"""
    return templates.TemplateResponse("settings/custom_fields.html", {
        "request": request,
        "user": current_user,
        "title": "Custom Fields"
    })

@router.get("/email-templates", response_class=HTMLResponse)
async def email_templates(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Show email templates management"""
    return templates.TemplateResponse("settings/email_templates.html", {
        "request": request,
        "user": current_user,
        "title": "Email Templates"
    })

@router.get("/invoice-groups", response_class=HTMLResponse)
async def invoice_groups(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Show invoice groups management"""
    return templates.TemplateResponse("settings/invoice_groups.html", {
        "request": request,
        "user": current_user,
        "title": "Invoice Groups"
    })

@router.get("/invoice-archive", response_class=HTMLResponse)
async def invoice_archive(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Show invoice archive settings"""
    return templates.TemplateResponse("settings/invoice_archive.html", {
        "request": request,
        "user": current_user,
        "title": "Invoice Archive"
    })

@router.get("/payment-methods", response_class=HTMLResponse)
async def payment_methods(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Show payment methods management"""
    return templates.TemplateResponse("settings/payment_methods.html", {
        "request": request,
        "user": current_user,
        "title": "Payment Methods"
    })

@router.get("/tax-rates", response_class=HTMLResponse)
async def tax_rates(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Show tax rates management"""
    return templates.TemplateResponse("settings/tax_rates.html", {
        "request": request,
        "user": current_user,
        "title": "Tax Rates"
    })

@router.get("/system", response_class=HTMLResponse)
async def system_settings(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Show system settings"""
    return templates.TemplateResponse("settings/system.html", {
        "request": request,
        "user": current_user,
        "title": "System Settings"
    })

@router.get("/import", response_class=HTMLResponse)
async def import_data(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Show data import functionality"""
    return templates.TemplateResponse("settings/import.html", {
        "request": request,
        "user": current_user,
        "title": "Import Data"
    })
