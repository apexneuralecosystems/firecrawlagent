import os
from apex import Client, set_default_client
from app.models.user import User
from app.models.organization import Organization
from app.models.payment import Payment

# Store the client instance globally
_apex_client = None

def init_apex():
    global _apex_client
    # Use Postgres from ENV
    database_url = os.getenv("DATABASE_URL", "postgresql+asyncpg://devulapellykushalkumarreddy@localhost/firecrawlagent")
    
    print(f"🔌 Apex Client connecting to: {database_url}")
    
    client = Client(
        database_url=database_url,
        user_model=User,
        organization_model=Organization,
        secret_key=os.getenv("SECRET_KEY", "default-dev-secret-key"),
    )

    set_default_client(client)
    _apex_client = client
    
    return client

def get_apex_client():
    """Get the initialized apex client instance."""
    global _apex_client
    if _apex_client is None:
        _apex_client = init_apex()
    return _apex_client

async def init_apex_async():
    """Initialize apex client in async context."""
    client = init_apex()
    return client
