"""
FastAPI application - takes user input and calls functions from app.py.
"""
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from apex import bootstrap
from app import (
    user_signup,
    user_login,
    user_logout,
    user_forgot_password,
    user_reset_password,
    payment_create_order,
    payment_capture_order,
    payment_get_order
)

app = FastAPI(title="My App API", version="1.0.0")
logger = logging.getLogger(__name__)

# Bootstrap database on startup (async context)
# Tables are automatically created when the app starts
@app.on_event("startup")
async def startup_event():
    """Initialize database tables automatically on application startup."""
    try:
        # In async context, bootstrap() returns a coroutine that should be awaited
        result = bootstrap()
        if hasattr(result, '__await__'):  # It's a coroutine
            await result
            print("✓ Database tables created successfully on startup")
        # If not a coroutine, it already ran synchronously
    except Exception as e:
        print(f"Warning: Database bootstrap failed: {e}")
        print("Server will start but database operations may fail until database is available.")

# ============================================
# Request Models
# ============================================

class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: str = None
    last_name: str = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

class CreateOrderRequest(BaseModel):
    amount: float
    currency: str = "USD"
    description: str = None

class CaptureOrderRequest(BaseModel):
    order_id: str

# ============================================
# Authentication Endpoints
# ============================================

@app.post("/api/signup")
def signup_endpoint(request: SignupRequest):
    """User signup endpoint."""
    try:
        user = user_signup(
            email=request.email,
            password=request.password,
            first_name=request.first_name,
            last_name=request.last_name
        )
        return {
            "message": "User created successfully",
            "user_id": str(user.id),
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/login")
def login_endpoint(request: LoginRequest):
    """User login endpoint."""
    try:
        tokens = user_login(email=request.email, password=request.password)
        return tokens
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid email or password")

@app.post("/api/logout")
def logout_endpoint():
    """User logout endpoint."""
    result = user_logout()
    return result

@app.post("/api/forgot-password")
def forgot_password_endpoint(request: ForgotPasswordRequest):
    """Forgot password endpoint."""
    try:
        return user_forgot_password(email=request.email)
    except Exception as e:
        logger.exception("Forgot password request failed for %s", request.email)
        # Always return success to prevent email enumeration
        return {
            "message": "If the email exists, a password reset link has been sent",
            "success": True
        }

@app.post("/api/reset-password")
def reset_password_endpoint(request: ResetPasswordRequest):
    """Reset password endpoint."""
    try:
        result = user_reset_password(token=request.token, new_password=request.new_password)
        if result["success"]:
            return result
        else:
            logger.warning("Password reset failed for token %s: %s", request.token, result["message"])
            raise HTTPException(status_code=400, detail=result["message"])
    except Exception as e:
        logger.exception("Password reset endpoint error")
        raise HTTPException(status_code=400, detail=str(e))

# ============================================
# Payment Endpoints
# ============================================

@app.post("/api/payments/create-order")
def create_order_endpoint(request: CreateOrderRequest):
    """Create PayPal order endpoint."""
    try:
        order = payment_create_order(
            amount=request.amount,
            currency=request.currency,
            description=request.description
        )
        return order
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/payments/capture-order")
def capture_order_endpoint(request: CaptureOrderRequest):
    """Capture PayPal order endpoint."""
    try:
        capture = payment_capture_order(order_id=request.order_id)
        return capture
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/payments/order/{order_id}")
def get_order_endpoint(order_id: str):
    """Get PayPal order by ID endpoint."""
    try:
        order = payment_get_order(order_id=order_id)
        return order
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

# ============================================
# Root Endpoint
# ============================================

@app.get("/")
def root():
    return {
        "message": "API is running",
        "status": "healthy",
        "docs": "/docs",
        "endpoints": {
            "auth": [
                "POST /api/signup",
                "POST /api/login",
                "POST /api/logout",
                "POST /api/forgot-password",
                "POST /api/reset-password"
            ],
            "payments": [
                "POST /api/payments/create-order",
                "POST /api/payments/capture-order",
                "GET /api/payments/order/{order_id}"
            ]
        }
    }