import hmac
import hashlib
import time
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from app.config import get_settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

# Simple in-memory rate limiting store
rate_limit_store = {}

def verify_api_key(api_key: str) -> bool:
    settings = get_settings()
    return hmac.compare_digest(api_key, settings.secret_key)

async def get_api_key_header(api_key: str = Security(api_key_header)):
    if not verify_api_key(api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )
    return api_key

def verify_webhook_signature(payload: bytes, signature: str, secret: str) -> bool:
    expected_signature = hmac.new(
        key=secret.encode("utf-8"),
        msg=payload,
        digestmod=hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(expected_signature, signature)

def check_rate_limit(identifier: str, max_requests: int = 10, window_seconds: int = 60) -> bool:
    """
    Simple rate limiting implementation.
    """
    now = time.time()
    
    if identifier not in rate_limit_store:
        rate_limit_store[identifier] = []
        
    # Clean up old timestamps
    rate_limit_store[identifier] = [ts for ts in rate_limit_store[identifier] if now - ts < window_seconds]
    
    if len(rate_limit_store[identifier]) >= max_requests:
        return False
        
    rate_limit_store[identifier].append(now)
    return True
