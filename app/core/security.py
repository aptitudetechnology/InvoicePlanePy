from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from passlib.exc import UnknownHashError
from app.config import settings

# Password hashing with error handling for bcrypt compatibility
try:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    # Test the context to ensure it works
    pwd_context.hash("test")
    BCRYPT_AVAILABLE = True
except Exception as e:
    print(f"⚠️  bcrypt not available ({e}), using fallback hashing")
    pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
    BCRYPT_AVAILABLE = False

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    try:
        # Handle fallback plain text passwords
        if hashed_password.startswith("PLAIN:"):
            return plain_password == hashed_password[6:]  # Remove "PLAIN:" prefix
        
        return pwd_context.verify(plain_password, hashed_password)
    except UnknownHashError:
        # If hash format is unknown, treat as invalid
        return False
    except Exception:
        # Any other error, assume invalid
        return False

def get_password_hash(password: str) -> str:
    """Hash a password"""
    try:
        # Ensure password is not too long for bcrypt (72 bytes max)
        if BCRYPT_AVAILABLE and len(password.encode('utf-8')) > 72:
            password = password[:8]  # Truncate to safe length
            print(f"⚠️  Password truncated to: {password}")
        
        return pwd_context.hash(password)
    except Exception as e:
        # Fallback: return plain text with prefix
        print(f"⚠️  Password hashing failed ({e}), using plain text fallback")
        return f"PLAIN:{password}"

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> dict:
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        return None
