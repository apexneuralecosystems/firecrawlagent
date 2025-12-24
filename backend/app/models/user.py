from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, UUID
from apex import Model, ID, Timestamps, register_model

@register_model
class User(Model, ID, Timestamps):
    __tablename__ = "users"

    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=True, index=True)

    password_hash = Column(String(255), nullable=False)

    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)

    phone = Column(String(30), nullable=True)
    country = Column(String(100), nullable=True)

    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_org_admin = Column(Boolean, default=False, nullable=False)

    # SaaS link
    organization_id = Column(UUID, ForeignKey("organizations.id"), nullable=True, index=True)

    # security / reset
    reset_token = Column(String(255), nullable=True, index=True)
    reset_token_expires = Column(String(255), nullable=True)
    login_attempts = Column(Integer, default=0, nullable=False)
    locked_until = Column(String(255), nullable=True)
