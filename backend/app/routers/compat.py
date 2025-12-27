"""
Compatibility router that mirrors the `packagereference/` API surface.

packagereference endpoints:
  - POST /api/signup
  - POST /api/login
  - POST /api/logout
  - POST /api/forgot-password
  - POST /api/reset-password

Our project historically uses:
  - /api/auth/signup, /api/auth/login, /api/auth/forgot-password, /api/auth/reset-password, /api/auth/me

This router provides aliases with the same shapes as packagereference, while keeping our
loop-safe async Apex integration (no apex.sync wrappers).
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr

from app.apex_client import get_apex_client
from app.deps.auth import get_current_user
from apex.domain.services.auth import AuthService
from apex.domain.services.password_reset import PasswordResetService
from apex.domain.services.password_reset_sendgrid import PasswordResetWithEmailService
from apex.domain.services.user import UserService
from apex.infrastructure.email.sendgrid import SendGridEmailAdapter

import logging
import os
from app.config import get_settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["Compat"])


class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: str | None = None
    last_name: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


@router.post("/signup")
async def signup_endpoint(request: SignupRequest):
    """Mirrors packagereference: returns message + user fields."""
    client = get_apex_client()
    async with client.get_session() as session:
        user_service = UserService(session=session, user_model=client.user_model)
        user = await user_service.create_user(
            email=request.email,
            password=request.password,
            first_name=request.first_name,
            last_name=request.last_name,
        )
        await session.commit()
        return {
            "message": "User created successfully",
            "user_id": str(user.id),
            "email": user.email,
            "first_name": getattr(user, "first_name", None),
            "last_name": getattr(user, "last_name", None),
        }


@router.post("/login")
async def login_endpoint(request: LoginRequest):
    """Mirrors packagereference: returns tokens dict."""
    client = get_apex_client()
    async with client.get_session() as session:
        auth_service = AuthService(session=session, user_model=client.user_model, secret_key=client.secret_key)
        user = await auth_service.authenticate_user(email=request.email, password=request.password)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        tokens = await auth_service.create_tokens(user)
        await session.commit()
        return tokens


@router.post("/logout")
async def logout_endpoint():
    """Mirrors packagereference: stateless logout."""
    return {"message": "Logged out successfully", "success": True}


@router.post("/forgot-password")
async def forgot_password_endpoint(request: ForgotPasswordRequest):
    """
    Mirrors packagereference behavior: always returns success to prevent enumeration.
    Uses SendGrid if configured; otherwise prints dev token to logs.
    """
    frontend_reset_url = os.getenv("FRONTEND_RESET_URL", "http://localhost:3000/reset-password")
    client = get_apex_client()

    try:
        email_adapter = SendGridEmailAdapter()
        if email_adapter.enabled:
            async with client.get_session() as session:
                reset_service = PasswordResetWithEmailService(
                    session=session,
                    user_model=client.user_model,
                    email_adapter=email_adapter,
                )
                await reset_service.request_password_reset(request.email)
        else:
            # Dev mode: generate token and print
            async with client.get_session() as session:
                reset_service = PasswordResetService(session=session, user_model=client.user_model)
                user, token = await reset_service.request_password_reset(request.email)
                await session.commit()
                if user and token and not get_settings().is_production:
                    reset_link = f"{frontend_reset_url}?token={token}"
                    logger.info("Generated password reset token for %s (dev mode): %s", request.email, reset_link)
                    print("\n" + "=" * 60)
                    print("⚠️  SENDGRID_API_KEY not configured, using dev-mode reset link")
                    print(f"Email: {request.email}")
                    print(f"Reset Link: {reset_link}")
                    print(f"Token: {token}")
                    print("=" * 60 + "\n")
    except Exception:
        logger.exception("Forgot password request failed for %s", request.email)

    return {
        "message": "If the email exists, a password reset link has been sent",
        "success": True,
    }


@router.post("/reset-password")
async def reset_password_endpoint(request: ResetPasswordRequest):
    """Mirrors packagereference: returns {message, success}."""
    client = get_apex_client()
    async with client.get_session() as session:
        reset_service = PasswordResetService(session=session, user_model=client.user_model)
        success = await reset_service.reset_password(token=request.token, new_password=request.new_password)
        await session.commit()

    if not success:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    return {"message": "Password reset successfully", "success": True}


@router.get("/me")
async def me_endpoint(user=Depends(get_current_user)):
    """Convenience alias for /api/auth/me (not in packagereference, requested as authme)."""
    return user


