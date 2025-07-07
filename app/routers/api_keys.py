from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
import secrets
import hashlib
from datetime import datetime

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.api_key import ApiKey

router = APIRouter()

class ApiKeyResponse(BaseModel):
    id: int
    name: str | None
    key_prefix: str
    is_active: bool
    created_at: datetime
    last_used_at: datetime | None

class ApiKeyCreate(BaseModel):
    name: str | None = None

class GeneratedApiKey(BaseModel):
    key: str
    key_info: ApiKeyResponse

@router.get("/keys", response_model=list[ApiKeyResponse])
async def list_api_keys(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all API keys for the current user"""
    keys = db.query(ApiKey).filter(ApiKey.user_id == current_user.id).all()
    return keys

@router.post("/keys/generate", response_model=GeneratedApiKey)
async def generate_api_key(
    key_data: ApiKeyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate a new API key"""
    # Generate a secure random key
    raw_key = f"sk_{secrets.token_urlsafe(32)}"
    
    # Hash the key for storage
    key_hash = hashlib.sha256(raw_key.encode()).hexdigest()
    
    # Create the API key record
    api_key = ApiKey(
        key_hash=key_hash,
        key_prefix=raw_key[:8],  # Store first 8 chars for display
        name=key_data.name,
        user_id=current_user.id
    )
    
    db.add(api_key)
    db.commit()
    db.refresh(api_key)
    
    # Return the key info with the actual key (only time it's shown)
    key_info = ApiKeyResponse(
        id=api_key.id,
        name=api_key.name,
        key_prefix=api_key.key_prefix,
        is_active=api_key.is_active,
        created_at=api_key.created_at,
        last_used_at=api_key.last_used_at
    )
    
    return GeneratedApiKey(key=raw_key, key_info=key_info)

@router.delete("/keys/{key_id}")
async def delete_api_key(
    key_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete an API key"""
    api_key = db.query(ApiKey).filter(
        ApiKey.id == key_id,
        ApiKey.user_id == current_user.id
    ).first()
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )
    
    db.delete(api_key)
    db.commit()
    
    return JSONResponse({"message": "API key deleted successfully"})

@router.patch("/keys/{key_id}/toggle")
async def toggle_api_key(
    key_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Toggle API key active status"""
    api_key = db.query(ApiKey).filter(
        ApiKey.id == key_id,
        ApiKey.user_id == current_user.id
    ).first()
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )
    
    api_key.is_active = not api_key.is_active
    db.commit()
    
    return JSONResponse({"message": f"API key {'activated' if api_key.is_active else 'deactivated'}"})

# API key authentication dependency
def get_api_key_user(
    api_key: str = Depends(lambda: None),  # This would be extracted from Authorization header
    db: Session = Depends(get_db)
) -> User:
    """Authenticate user via API key"""
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key required"
        )
    
    # Hash the provided key
    key_hash = hashlib.sha256(api_key.encode()).hexdigest()
    
    # Find the API key
    api_key_record = db.query(ApiKey).filter(
        ApiKey.key_hash == key_hash,
        ApiKey.is_active == True
    ).first()
    
    if not api_key_record:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    
    # Update last used timestamp
    api_key_record.last_used_at = datetime.utcnow()
    db.commit()
    
    return api_key_record.user
