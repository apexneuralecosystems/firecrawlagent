from fastapi import Header, HTTPException
from apex.auth import verify_token
from apex.users import get_user

def get_current_user(authorization: str = Header(None)):
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing Bearer token")

    token = authorization.split(" ", 1)[1].strip()

    try:
        payload = verify_token(token=token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid/expired token")

    user_id = payload.get("sub")
    user = get_user(user_id=user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found/inactive")

    return user

def require_admin(user= None, authorization: str = Header(None)):
    user = user or get_current_user(authorization)
    if not getattr(user, "is_superuser", False):
        raise HTTPException(status_code=403, detail="Admin only")
    return user
