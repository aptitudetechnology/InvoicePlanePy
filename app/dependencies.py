from fastapi import Depends, HTTPException, status, Cookie
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session, joinedload
from typing import Optional
from datetime import datetime
from app.database import get_db
from app.models.user import User
from app.models.api_key import ApiKey
from app.core.security import verify_token
import hashlib

security = HTTPBearer(auto_error=False)

def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    session_token: Optional[str] = Cookie(None),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """Get current user if authenticated (optional)"""
    token = None

    # Try to get token from Authorization header first
    if credentials:
        token = credentials.credentials

        # Check if it's an API key (starts with 'sk_')
        if token.startswith('sk_'):
            return _authenticate_api_key(token, db)

    # Fall back to session cookie
    elif session_token:
        token = session_token

    if not token:
        return None

    payload = verify_token(token)
    if not payload:
        return None

    user_id = payload.get("sub")
    if user_id is None:
        return None

    user = db.query(User).filter(User.id == user_id).first()
    return user

def _authenticate_api_key(api_key: str, db: Session) -> Optional[User]:
    """Authenticate using API key"""
    try:
        print(f"DEBUG: Authenticating API key: {api_key[:10]}...")
        
        # Hash the provided key
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        print(f"DEBUG: Generated hash: {key_hash}")

        # Find the API key in database with user relationship loaded
        api_key_record = db.query(ApiKey).options(
            joinedload(ApiKey.user)
        ).filter(
            ApiKey.key_hash == key_hash,
            ApiKey.is_active == True
        ).first()

        if not api_key_record:
            print(f"DEBUG: No API key record found for hash")
            return None

        print(f"DEBUG: Found API key record: ID={api_key_record.id}, UserID={api_key_record.user_id}")

        # Check if key has expired
        if api_key_record.expires_at and datetime.utcnow() > api_key_record.expires_at:
            print(f"DEBUG: API key has expired")
            return None

        # Update last used timestamp
        api_key_record.last_used_at = datetime.utcnow()
        db.commit()
        print(f"DEBUG: Updated last_used_at timestamp")

        # Return the associated user (should be loaded due to joinedload)
        user = api_key_record.user
        if not user:
            print(f"DEBUG: No user associated with API key")
            return None
            
        if not user.is_active:
            print(f"DEBUG: User is not active")
            return None
            
        print(f"DEBUG: Authentication successful for user: {user.username}")
        return user

    except Exception as e:
        print(f"DEBUG: API key authentication error: {e}")
        import traceback
        traceback.print_exc()
        return None

def get_current_user(current_user: Optional[User] = Depends(get_current_user_optional)) -> User:
    """Get current authenticated user (required)"""
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    return current_user

def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Require admin privileges"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user
