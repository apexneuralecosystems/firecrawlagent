from fastapi import Header, HTTPException
from apex.core.security.jwt import decode_token
from apex.domain.services.user import UserService
from app.apex_client import get_apex_client

async def get_current_user(authorization: str = Header(None)):
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing Bearer token")

    token = authorization.split(" ", 1)[1].strip()

    try:
        client = get_apex_client()
        payload = decode_token(token, secret_key=client.secret_key)
        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Invalid/expired token")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid/expired token")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid/expired token")

    async with client.get_session() as session:
        user_service = UserService(session=session, user_model=client.user_model)
        user = await user_service.get_user_by_id(user_id)
        if not user or (hasattr(user, "is_active") and not user.is_active):
            raise HTTPException(status_code=401, detail="User not found/inactive")

    return user

async def require_admin(user=None, authorization: str = Header(None)):
    user = user or await get_current_user(authorization)
    if not getattr(user, "is_superuser", False):
        raise HTTPException(status_code=403, detail="Admin only")
    return user
