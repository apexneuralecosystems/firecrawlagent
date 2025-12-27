"""
Database models for authentication and payments.
"""
from sqlalchemy import Column, String, Boolean, Numeric
from apex.models import Model, ID, Timestamps, register_model


@register_model
class User(Model, ID, Timestamps):
    """User model for authentication."""
    __tablename__ = "users"
    
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    username = Column(String(100), unique=True, nullable=True, index=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    phone = Column(String(50), nullable=True)
    country = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)


@register_model
class Payment(Model, ID, Timestamps):
    """Payment model for payment tracking."""
    __tablename__ = "payments"
    
    paypal_order_id = Column(String(100), unique=True, nullable=False)
    paypal_capture_id = Column(String(100), unique=True, nullable=True)
    amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(10), default="USD", nullable=False)
    status = Column(String(50), default="created", nullable=False)
    payment_method = Column(String(50), default="paypal", nullable=False)
    user_id = Column(String(36), nullable=True)  # UUID as string