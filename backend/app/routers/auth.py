from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from apex.auth import signup, login, refresh_token, forgot_password, reset_password, change_password
from app.deps.auth import get_current_user
from app.apex_client import get_apex_client
from apex.domain.services.password_reset_sendgrid import PasswordResetWithEmailService
from apex.infrastructure.email.sendgrid import SendGridEmailAdapter
import logging
import os

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.get("/me")
def api_me(user=Depends(get_current_user)):
    return user


class SignupIn(BaseModel):
    email: EmailStr
    password: str
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None

@router.post("/signup")
def api_signup(data: SignupIn):
    try:
        user = signup(**data.model_dump())
        return {"id": user.id, "email": user.email}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

class LoginIn(BaseModel):
    email: EmailStr
    password: str

@router.post("/login")
def api_login(data: LoginIn):
    try:
        return login(email=data.email, password=data.password)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

class RefreshIn(BaseModel):
    refresh_token: str

@router.post("/refresh")
def api_refresh(data: RefreshIn):
    try:
        return refresh_token(refresh_token=data.refresh_token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

class ForgotIn(BaseModel):
    email: EmailStr

@router.post("/forgot-password")
async def api_forgot(data: ForgotIn):
    """
    Request password reset via email.
    Uses SendGrid if configured, otherwise uses basic apex forgot_password.
    Following demopackage pattern but with SendGrid enhancement.
    """
    try:
        # Check if SendGrid is configured
        email_adapter = SendGridEmailAdapter()
        
        if email_adapter.enabled:
            # Use SendGrid service to send email
            try:
                client = get_apex_client()
                async with client.get_session() as session:
                    reset_service = PasswordResetWithEmailService(
                        session=session,
                        user_model=client.user_model,
                        email_adapter=email_adapter
                    )
                    success = await reset_service.request_password_reset(data.email)
                    
                    if success:
                        logger.info(f"Password reset email sent to {data.email}")
            except Exception as e:
                logger.error(f"SendGrid email sending failed: {str(e)}")
                # Fall through to basic forgot_password as fallback
                user, token = forgot_password(email=data.email)
        else:
            # SendGrid not configured - use basic apex forgot_password (like demopackage)
            logger.warning("SendGrid not configured. Using basic password reset.")
            print(f"\n{'='*60}")
            print(f"⚠️  SendGrid Email Not Configured")
            print(f"{'='*60}")
            print(f"To enable email sending, add to your .env file:")
            print(f"  SEND_GRID_API=your_sendgrid_api_key")
            print(f"  FROM_EMAIL=noreply@yourdomain.com")
            print(f"  FROM_NAME=Firecrawl Agent")
            print(f"{'='*60}\n")
            
            # Use basic forgot_password from apex (same as demopackage)
            user, token = forgot_password(email=data.email)
            
            if user and token:
                # Get frontend reset URL from environment variable
                frontend_reset_url = os.getenv('FRONTEND_RESET_URL', 'http://localhost:3000/reset-password')
                reset_link = f"{frontend_reset_url}?token={token}"
                logger.info(f"Password reset token generated for {data.email}: {reset_link}")
                print(f"\n{'='*60}")
                print(f"🔑 PASSWORD RESET TOKEN (Development Mode)")
                print(f"{'='*60}")
                print(f"Email: {data.email}")
                print(f"Reset Link: {reset_link}")
                print(f"Token: {token}")
                print(f"{'='*60}\n")
        
        # Always return success to prevent email enumeration (like demopackage)
        return {
            "message": "If the email exists, a password reset link has been sent",
            "success": True
        }
            
    except Exception as e:
        logger.error(f"Password reset error: {str(e)}", exc_info=True)
        print(f"❌ Password reset error: {str(e)}")
        # Always return success to prevent email enumeration (like demopackage)
        return {
            "message": "If the email exists, a password reset link has been sent",
            "success": True
        }

class ResetIn(BaseModel):
    token: str
    new_password: str

@router.post("/reset-password")
def api_reset(data: ResetIn):
    try:
        ok = reset_password(token=data.token, new_password=data.new_password)
        return {"ok": ok}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

class ChangeIn(BaseModel):
    user_id: str
    old_password: str
    new_password: str

@router.post("/change-password")
def api_change(data: ChangeIn):
    ok = change_password(**data.model_dump())
    return {"ok": ok}
