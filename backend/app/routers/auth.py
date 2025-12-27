from typing import Any

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from app.deps.auth import get_current_user
from app.apex_client import get_apex_client
from apex.domain.services.password_reset import PasswordResetService
from apex.domain.services.password_reset_sendgrid import PasswordResetWithEmailService
from apex.infrastructure.email.sendgrid import SendGridEmailAdapter
from apex.domain.services.auth import AuthService
from apex.domain.services.user import UserService
import logging
import os
from app.config import get_settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.get("/me")
async def api_me(user=Depends(get_current_user)):
    return user


class SignupIn(BaseModel):
    email: EmailStr
    password: str
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None

@router.post("/signup")
async def api_signup(data: SignupIn):
    try:
        client = get_apex_client()
        async with client.get_session() as session:
            user_service = UserService(session=session, user_model=client.user_model)
            user = await user_service.create_user(**data.model_dump())
            await session.commit()
        return {"id": user.id, "email": user.email}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

class LoginIn(BaseModel):
    email: EmailStr
    password: str

@router.post("/login")
async def api_login(data: LoginIn):
    try:
        client = get_apex_client()
        async with client.get_session() as session:
            auth_service = AuthService(session=session, user_model=client.user_model, secret_key=client.secret_key)
            user = await auth_service.authenticate_user(email=data.email, password=data.password)
            if not user:
                raise HTTPException(status_code=401, detail="Invalid credentials")
            tokens = await auth_service.create_tokens(user)
            await session.commit()
            return tokens
    except Exception as e:
        if isinstance(e, HTTPException):
            raise
        raise HTTPException(status_code=400, detail=str(e))

class RefreshIn(BaseModel):
    refresh_token: str

@router.post("/refresh")
async def api_refresh(data: RefreshIn):
    try:
        client = get_apex_client()
        async with client.get_session() as session:
            auth_service = AuthService(session=session, user_model=client.user_model, secret_key=client.secret_key)
            refreshed = await auth_service.refresh_access_token(refresh_token=data.refresh_token)
            if not refreshed:
                raise HTTPException(status_code=401, detail="Invalid refresh token")
            await session.commit()
            return refreshed
    except Exception as e:
        if isinstance(e, HTTPException):
            raise
        raise HTTPException(status_code=401, detail=str(e))

class ForgotIn(BaseModel):
    email: EmailStr

async def _generate_basic_reset_token(email: str, client) -> tuple[Any, str | None]:
    """Generate and persist a reset token without sending email."""
    async with client.get_session() as session:
        reset_service = PasswordResetService(session=session, user_model=client.user_model)
        user, token = await reset_service.request_password_reset(email)
        await session.commit()
        return user, token

async def _log_dev_mode_token(email: str, client, frontend_reset_url: str):
    """Log the reset token when no email delivery is configured."""
    if get_settings().is_production:
        return
    user, token = await _generate_basic_reset_token(email, client)
    if user and token:
        reset_link = f"{frontend_reset_url}?token={token}"
        logger.info(f"Password reset token generated for {email}: {reset_link}")
        print(f"\n{'='*60}")
        print("🔑 PASSWORD RESET TOKEN (Development Mode)")
        print(f"{'='*60}")
        print(f"Email: {email}")
        print(f"Reset Link: {reset_link}")
        print(f"Token: {token}")
        print(f"{'='*60}\n")

@router.post("/forgot-password")
async def api_forgot(data: ForgotIn):
    """
    Request password reset via email.
    Uses SendGrid if configured, otherwise falls back to logging the token for dev mode.
    """
    frontend_reset_url = os.getenv('FRONTEND_RESET_URL', 'http://localhost:3000/reset-password')
    client = get_apex_client()
    try:
        email_adapter = SendGridEmailAdapter()
        if email_adapter.enabled:
            try:
                async with client.get_session() as session:
                    reset_service = PasswordResetWithEmailService(
                        session=session,
                        user_model=client.user_model,
                        email_adapter=email_adapter
                    )
                    success = await reset_service.request_password_reset(data.email)
                    if success:
                        logger.info(f"Password reset email sent to {data.email}")
            except Exception as exc:
                logger.error(f"SendGrid email sending failed: {str(exc)}")
                await _log_dev_mode_token(data.email, client, frontend_reset_url)
        else:
            logger.warning("SendGrid not configured. Using basic password reset.")
            print(f"\n{'='*60}")
            print("⚠️  SendGrid Email Not Configured")
            print(f"{'='*60}")
            print("To enable email sending, add to your .env file:")
            print("  SENDGRID_API_KEY=your_sendgrid_api_key")
            print("  FROM_EMAIL=noreply@yourdomain.com")
            print("  FROM_NAME=Firecrawl Agent")
            print(f"{'='*60}\n")
            await _log_dev_mode_token(data.email, client, frontend_reset_url)

        return {
            "message": "If the email exists, a password reset link has been sent",
            "success": True
        }
    except Exception as exc:
        logger.error(f"Password reset error: {str(exc)}", exc_info=True)
        print(f"❌ Password reset error: {str(exc)}")
        return {
            "message": "If the email exists, a password reset link has been sent",
            "success": True
        }

class ResetIn(BaseModel):
    token: str
    new_password: str

@router.post("/reset-password")
async def api_reset(data: ResetIn):
    try:
        client = get_apex_client()
        async with client.get_session() as session:
            reset_service = PasswordResetService(session=session, user_model=client.user_model)
            ok = await reset_service.reset_password(token=data.token, new_password=data.new_password)
            await session.commit()
        return {"ok": ok}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

class ChangeIn(BaseModel):
    user_id: str
    old_password: str
    new_password: str

@router.post("/change-password")
async def api_change(data: ChangeIn):
    client = get_apex_client()
    async with client.get_session() as session:
        user_service = UserService(session=session, user_model=client.user_model)
        user = await user_service.get_user_by_id(data.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        ok = await user_service.change_password(user=user, old_password=data.old_password, new_password=data.new_password)
        await session.commit()
        return {"ok": ok}
