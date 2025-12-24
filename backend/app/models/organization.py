from sqlalchemy import Column, String, Boolean
from apex import Model, ID, Timestamps, register_model

@register_model
class Organization(Model, ID, Timestamps):
    __tablename__ = "organizations"

    name = Column(String(255), nullable=False)
    slug = Column(String(100), unique=True, nullable=True, index=True)

    email = Column(String(255), nullable=True)
    phone = Column(String(30), nullable=True)
    address = Column(String(500), nullable=True)
    country = Column(String(100), nullable=True)

    is_active = Column(Boolean, default=True, nullable=False)
