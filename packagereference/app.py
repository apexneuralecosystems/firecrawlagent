

"""
Authentication and payment functions.
"""
import logging
import os
from dotenv import load_dotenv
from apex import Client, set_default_client, bootstrap
from apex.auth import signup, login, forgot_password, reset_password
from apex.payments import create_order, capture_order, get_order
from models import User, Payment

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

# Get database URL and ensure it uses asyncpg driver
db_url = os.getenv('DATABASE_URL', 'postgresql+asyncpg://pra_user:StrongPass@localhost:5432/pra')
# If URL uses postgresql:// without a driver, add +asyncpg
if db_url.startswith('postgresql://') and '+asyncpg' not in db_url and '+psycopg' not in db_url:
    db_url = db_url.replace('postgresql://', 'postgresql+asyncpg://', 1)

# Initialize client (auto-detects async/sync from URL or DB_ASYNC_MODE)
client = Client(
    database_url=db_url,
    user_model=User,
    secret_key=os.getenv('SECRET_KEY', 'your-secret-key-minimum-32-characters-long'),
    async_mode=True
)

# Set default client
set_default_client(client)

# Bootstrap will be called on FastAPI startup event (see main.py)
# This avoids calling it at module import time which can cause coroutine warnings
# Tables are automatically created from your models (User, Payment) on startup


# ============================================
# Authentication Functions
# ============================================

def user_signup(email: str, password: str, first_name: str = None, last_name: str = None):
    """Signup a new user."""
    return signup(email=email, password=password, first_name=first_name, last_name=last_name)


def user_login(email: str, password: str):
    """Login user and get tokens."""
    return login(email=email, password=password)


def user_logout():
    """Logout user."""
    return {"message": "Logged out successfully", "success": True}


def user_forgot_password(email: str):
    """Request password reset with optional dev-mode logging."""
    try:
        user, reset_token = forgot_password(email=email)
        if reset_token and not os.getenv("SENDGRID_API_KEY"):
            frontend_reset_url = os.getenv("FRONTEND_RESET_URL", "http://localhost:3000/reset-password")
            reset_link = f"{frontend_reset_url}?token={reset_token}"
            logger.info("Generated password reset token for %s (dev mode): %s", email, reset_link)
            print("\n" + "=" * 60)
            print("⚠️  SENDGRID_API_KEY not configured, using dev-mode reset link")
            print(f"Email: {email}")
            print(f"Reset Link: {reset_link}")
            print(f"Token: {reset_token}")
            print("=" * 60 + "\n")
        return {
            "message": "If the email exists, a password reset link has been sent",
            "success": True
        }
    except Exception as exc:
        logger.exception("Password reset request failed for %s", email)
        return {
            "message": "If the email exists, a password reset link has been sent",
            "success": True
        }


def user_reset_password(token: str, new_password: str):
    """Reset password using token and report success/failure."""
    try:
        success = reset_password(token=token, new_password=new_password)
    except Exception as exc:
        logger.exception("Password reset failed for token %s", token)
        success = False

    return {
        "message": "Password reset successfully" if success else "Invalid or expired token",
        "success": success
    }


# ============================================
# Payment Functions
# ============================================

def payment_create_order(amount: float, currency: str = "USD", description: str = None):
    """Create PayPal order."""
    return create_order(amount=amount, currency=currency, description=description, save_to_db=True)


def payment_capture_order(order_id: str):
    """Capture PayPal order."""
    return capture_order(order_id=order_id, update_db=True)


def payment_get_order(order_id: str):
    """Get PayPal order by ID."""
    return get_order(order_id=order_id)