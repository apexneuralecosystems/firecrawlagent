"""
Payment router - PayPal integration.
"""
import os
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.deps.auth import get_current_user
from app.apex_client import get_apex_client

router = APIRouter(prefix="/api/payments", tags=["Payments"])


@router.get("/config")
async def check_paypal_config(user=Depends(get_current_user)):
    """Check PayPal configuration status."""
    paypal_client_id = os.getenv("PAYPAL_CLIENT_ID") or os.getenv("NEW_US_SANDBOX_CLIENT_ID")
    paypal_client_secret = os.getenv("PAYPAL_CLIENT_SECRET") or os.getenv("NEW_US_SANDBOX_SECRET")
    paypal_mode = os.getenv("PAYPAL_MODE", "sandbox")
    
    return {
        "configured": bool(paypal_client_id and paypal_client_secret),
        "has_client_id": bool(paypal_client_id),
        "has_client_secret": bool(paypal_client_secret),
        "mode": paypal_mode,
        "message": "PayPal is configured" if (paypal_client_id and paypal_client_secret) else "PayPal credentials are missing. Please set PAYPAL_CLIENT_ID and PAYPAL_CLIENT_SECRET in your .env file."
    }


class CreateOrderRequest(BaseModel):
    amount: float
    currency: str = "USD"
    description: str | None = None
    return_url: str | None = None
    cancel_url: str | None = None


class CaptureOrderRequest(BaseModel):
    order_id: str


@router.post("/create-order")
async def create_order_endpoint(request: CreateOrderRequest, user=Depends(get_current_user)):
    """Create PayPal order endpoint."""
    import traceback
    try:
        client = get_apex_client()

        # Get frontend base URL from environment variable
        frontend_base_url = os.getenv('FRONTEND_BASE_URL', 'http://localhost:3000')
        return_url = request.return_url or os.getenv('PAYPAL_RETURN_URL', f"{frontend_base_url}/payment")
        cancel_url = request.cancel_url or os.getenv('PAYPAL_CANCEL_URL', f"{frontend_base_url}/payment")

        return await client.payments.create_order(
            amount=request.amount,
            currency=request.currency,
            description=request.description,
            return_url=return_url,
            cancel_url=cancel_url,
            save_to_db=True
        )
    except ValueError as e:
        # PayPal configuration error
        error_msg = str(e)
        print(f"PayPal ValueError: {error_msg}")
        if "not configured" in error_msg.lower() or "required" in error_msg.lower():
            raise HTTPException(
                status_code=500,
                detail="PayPal is not configured. Please set PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET, and PAYPAL_MODE in your environment variables."
            )
        raise HTTPException(status_code=400, detail=error_msg)
    except RuntimeError as e:
        # Client not initialized error
        error_msg = str(e)
        print(f"PayPal RuntimeError: {error_msg}")
        if "no default client" in error_msg.lower():
            raise HTTPException(
                status_code=500,
                detail="Apex client not initialized. Please restart the server."
            )
        raise HTTPException(status_code=500, detail=error_msg)
    except Exception as e:
        error_msg = str(e)
        error_type = type(e).__name__
        print(f"PayPal Exception ({error_type}): {error_msg}")
        print(f"Traceback: {traceback.format_exc()}")
        
        # Check for PayPal authentication errors
        if "invalid_client" in error_msg.lower() or "authentication" in error_msg.lower() or "client authentication failed" in error_msg.lower():
            raise HTTPException(
                status_code=500,
                detail=f"PayPal authentication failed: {error_msg}. Please check your PAYPAL_CLIENT_ID and PAYPAL_CLIENT_SECRET in your environment variables."
            )
        # Check for configuration errors
        if "not configured" in error_msg.lower() or "required" in error_msg.lower():
            raise HTTPException(
                status_code=500,
                detail=f"PayPal configuration error: {error_msg}. Please set PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET, and PAYPAL_MODE in your environment variables."
            )
        raise HTTPException(status_code=400, detail=f"Payment error: {error_msg}")


@router.post("/capture-order")
async def capture_order_endpoint(request: CaptureOrderRequest, user=Depends(get_current_user)):
    """Capture PayPal order endpoint."""
    try:
        client = get_apex_client()
        return await client.payments.capture_order(
            order_id=request.order_id,
            update_db=True
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/order/{order_id}")
async def get_order_endpoint(order_id: str, user=Depends(get_current_user)):
    """Get PayPal order by ID endpoint."""
    try:
        client = get_apex_client()
        return await client.payments.paypal_service.get_order(order_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

