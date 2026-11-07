"""
Security, Cryptography, and Privacy utilities.
- Password hashing with bcrypt
- JWT Authentication token signing
- Reviewer PII pseudonymization via Salted SHA-256
"""
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Any, Union, Optional
import jwt
import bcrypt
from app.core.config import settings


def hash_password(password: str) -> str:
    """Hash a plaintext password securely using bcrypt."""
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against its bcrypt hash."""
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8")
        )
    except Exception:
        return False


def create_access_token(subject: Union[str, Any], role: str = "analyst", expires_delta: Optional[timedelta] = None) -> str:
    """Generate a signed JWT access token for user authentication."""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    payload = {
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "sub": str(subject),
        "role": role
    }
    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """Decode and validate a JWT token."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None


def pseudonymize_reviewer_id(raw_identifier: str) -> str:
    """
    Privacy Protection: Salts and hashes reviewer identities (email, username, IP)
    into a deterministic pseudonym so real identities are never exposed or stored.
    """
    if not raw_identifier:
        return "anon_unknown"
    salted = f"{settings.REVIEWER_HASH_SALT}::{raw_identifier.strip().lower()}"
    return hashlib.sha256(salted.encode("utf-8")).hexdigest()[:24]
