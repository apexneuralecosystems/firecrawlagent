"""
FastAPI Backend for FireCrawl Agent RAG Application
"""
# Disable ChromaDB telemetry before any chromadb import (avoids opentelemetry version conflicts)
import os
os.environ.setdefault("ANONYMIZED_TELEMETRY", "false")

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
import sys
import tempfile
import uuid
from datetime import datetime
from typing import Dict, Optional
from dotenv import load_dotenv
from app.apex_client import init_apex_async, get_apex_client
from app.config import get_settings, validate_production_env
from app.routers.auth import router as auth_router
from app.routers.compat import router as compat_router
from app.routers.payments import router as payments_router
from apex.infrastructure.email.sendgrid import SendGridEmailAdapter


# NOTE: We intentionally avoid custom `ssl` context hacks.
# If local certificate verification fails (common when Python isn't wired to macOS Keychain),
# we rely on the standard OpenSSL env var `SSL_CERT_FILE` to point at a CA bundle.
def _ensure_ssl_cert_file() -> None:
    """
    Best-effort: if SSL_CERT_FILE isn't set, try using certifi's CA bundle.
    This keeps the code aligned with upstream packages (no ssl monkeypatching),
    while fixing common macOS certificate store issues.
    """
    if os.getenv("SSL_CERT_FILE"):
        return
    try:
        import certifi  # type: ignore

        os.environ["SSL_CERT_FILE"] = certifi.where()
        print("🔒 Set SSL_CERT_FILE from certifi bundle for outbound HTTPS.")
    except Exception:
        # If certifi isn't installed, do nothing.
        return


# IMPORTANT: Add backend directory FIRST to avoid conflict with root app.py
# When we import 'app', we want backend/app/, not the root app.py file
backend_dir = os.path.dirname(__file__)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Also add project root for importing agentic_workflow and other root modules
# This goes AFTER backend_dir so 'app' resolves to backend/app/ first
project_root = os.path.dirname(backend_dir)
if project_root not in sys.path:
    sys.path.insert(1, project_root)  # Insert at position 1, not 0

# Load .env from project root (where .env file is located)
env_path = os.path.join(project_root, '.env')
load_dotenv(dotenv_path=env_path, override=True)

# Prevent root app.py from being accidentally imported
# This must happen after load_dotenv but before any imports that might trigger app.py
def _prevent_root_app_import():
    """Remove root app.py from sys.modules if it was accidentally imported."""
    if 'app' in sys.modules:
        app_module = sys.modules['app']
        if hasattr(app_module, '__file__') and app_module.__file__:
            app_file = app_module.__file__
            # Check if this is the root app.py (not backend/app/)
            if 'backend' not in app_file and app_file.endswith('app.py'):
                # This is the root app.py, not backend/app/
                # Remove it so backend/app/ can be imported instead
                del sys.modules['app']
                # Also remove any submodules
                modules_to_remove = [k for k in sys.modules.keys() if k.startswith('app.')]
                for mod_name in modules_to_remove:
                    del sys.modules[mod_name]

_prevent_root_app_import()

# Import WorkflowService at module level to avoid import issues
# This import happens after sys.path is configured and root app.py is prevented
# We need to ensure 'app' resolves to backend/app/, not root app.py
try:
    # Ensure root app.py is not imported before we try to import backend/app/
    _prevent_root_app_import()
    from app.services.workflow_service import WorkflowService
except (ImportError, ModuleNotFoundError) as e:
    # Fallback: try importing with explicit file path
    import importlib.util
    workflow_service_path = os.path.join(backend_dir, "app", "services", "workflow_service.py")
    if os.path.exists(workflow_service_path):
        spec = importlib.util.spec_from_file_location("app.services.workflow_service", workflow_service_path)
        workflow_service_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(workflow_service_module)
        WorkflowService = workflow_service_module.WorkflowService
    else:
        raise ImportError(f"Could not find workflow_service.py at {workflow_service_path}: {e}") from e

# IMPORTANT: Prevent nest_asyncio/uvloop conflicts
# nest_asyncio is only needed for Streamlit, not for FastAPI
# Uvloop conflicts with nest_asyncio, so we'll use standard asyncio
# Disable uvloop before uvicorn starts
os.environ["UVICORN_USE_UVLOOP"] = "0"

app = FastAPI(
    title="FireCrawl Agent API",
    version="1.0.0",
    description="REST API for FireCrawl Agent RAG Application"
)
@app.on_event("startup")
async def startup():
    settings = get_settings()
    validate_production_env(settings)
    _ensure_ssl_cert_file()
    await init_apex_async()

# CORS middleware
settings = get_settings()
allow_origins = settings.allowed_origins if settings.allowed_origins else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=False,  # Must be False when allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session storage.
# NOTE: This is not horizontally scalable. In production, run a SINGLE worker/replica unless you
# add a shared session/workflow store.
if settings.is_production and settings.require_single_worker:
    workers = os.getenv("WEB_CONCURRENCY") or os.getenv("UVICORN_WORKERS")
    if workers and workers.isdigit() and int(workers) > 1:
        raise RuntimeError(
            "WEB_CONCURRENCY/UVICORN_WORKERS > 1 is not supported with in-memory sessions. "
            "Set it to 1 or implement shared session storage."
        )
sessions: Dict[str, Dict] = {}

@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "message": "FireCrawl Agent API",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/api/health")
async def health_check():
    """Detailed health check."""
    return {
        "status": "healthy",
        "sessions": len(sessions),
        "environment": {
            "has_firecrawl_key": bool(os.getenv("FIRECRAWL_API_KEY")),
            "has_openrouter_key": bool(os.getenv("OPENROUTER_API_KEY")),
            "has_paypal_client_id": bool(os.getenv("PAYPAL_CLIENT_ID") or os.getenv("NEW_US_SANDBOX_CLIENT_ID")),
            "has_paypal_client_secret": bool(os.getenv("PAYPAL_CLIENT_SECRET") or os.getenv("NEW_US_SANDBOX_SECRET")),
            "paypal_mode": os.getenv("PAYPAL_MODE", "sandbox"),
        }
    }

@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and process a PDF document.
    
    Returns:
        Session ID and processing status
    """
    if not file.filename or not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )
    
    try:
        # WorkflowService is already imported at module level
        # Save uploaded file temporarily
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, file.filename)
            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)
            
            # Initialize workflow
            session_id = str(uuid.uuid4())
            workflow_service = WorkflowService()
            # process_document expects a directory path, not a file path
            workflow, collection_name = await workflow_service.process_document(temp_dir, session_id=session_id)
            
            sessions[session_id] = {
                "workflow": workflow,
                "collection_name": collection_name,
                "filename": file.filename,
                "uploaded_at": datetime.now().isoformat(),
                "file_size": len(content)
            }
            
            return {
                "session_id": session_id,
                "filename": file.filename,
                "status": "processed",
                "uploaded_at": sessions[session_id]["uploaded_at"]
            }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process document: {str(e)}"
        )

@app.post("/api/chat")
async def chat(query: dict):
    """
    Process a chat query.
    
    Request body:
        {
            "session_id": "uuid",
            "message": "user query"
        }
    """
    session_id = query.get("session_id")
    message = query.get("message")
    
    if not session_id:
        raise HTTPException(
            status_code=400,
            detail="session_id is required"
        )
    
    if session_id not in sessions:
        raise HTTPException(
            status_code=404,
            detail="Session not found. Please upload a document first."
        )
    
    if not message or not message.strip():
        raise HTTPException(
            status_code=400,
            detail="message is required"
        )
    
    try:
        # WorkflowService is already imported at module level
        workflow = sessions[session_id]["workflow"]
        workflow_service = WorkflowService()
        
        # Run workflow
        result, logs = await workflow_service.run_query(workflow, message.strip())
        
        response_text = result.response if hasattr(result, 'response') else str(result)
        
        return {
            "response": response_text,
            "session_id": session_id,
            "logs": logs if logs else None
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process query: {str(e)}"
        )

@app.get("/api/sessions/{session_id}")
async def get_session(session_id: str):
    """Get session information."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = sessions[session_id].copy()
    # Remove workflow object from response (not JSON serializable)
    session.pop("workflow", None)
    return session

@app.delete("/api/sessions/{session_id}")
async def delete_session(session_id: str):
    """Delete a session."""
    if session_id in sessions:
        try:
            WorkflowService.delete_vector_collection_for_session(session_id)
        except Exception as e:
            print(f"Warning: vector collection cleanup failed for {session_id}: {e}")
        del sessions[session_id]
        return {"status": "deleted", "session_id": session_id}
    return {"status": "not_found", "session_id": session_id}

@app.get("/api/sessions")
async def list_sessions():
    """List all active sessions."""
    session_list = []
    for session_id, session_data in sessions.items():
        session_info = {
            "session_id": session_id,
            "filename": session_data.get("filename"),
            "uploaded_at": session_data.get("uploaded_at"),
            "file_size": session_data.get("file_size")
        }
        session_list.append(session_info)
    return {"sessions": session_list, "count": len(session_list)}

# ============================================
# Newsletter Subscription Endpoint
# ============================================

class NewsletterRequest(BaseModel):
    email: EmailStr

@app.post("/api/newsletter/subscribe")
async def newsletter_subscribe(request: NewsletterRequest):
    """
    Subscribe to newsletter and send welcome email via SendGrid.
    """
    try:
        email_adapter = SendGridEmailAdapter()
        
        if not email_adapter.enabled:
            return {
                "success": False,
                "message": "Email service is not configured. Please contact support."
            }
        
        # Get frontend base URL from environment variable
        frontend_base_url = os.getenv('FRONTEND_BASE_URL', 'http://localhost:3000')
        
        # Predefined welcome message
        subject = "Welcome to Firecrawl Agent - Stay Updated!"
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #4F46E5, #818CF8); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9fafb; padding: 30px; border-radius: 0 0 10px 10px; }}
                .button {{ display: inline-block; padding: 12px 24px; background: #4F46E5; color: white; text-decoration: none; border-radius: 6px; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 30px; color: #6b7280; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>⚡ Welcome to Firecrawl Agent!</h1>
                </div>
                <div class="content">
                    <p>Hi there,</p>
                    <p>Thank you for subscribing to our newsletter! We're excited to have you on board.</p>
                    <p>You'll now receive the latest updates on:</p>
                    <ul>
                        <li>🔍 Agentic RAG and AI search innovations</li>
                        <li>🚀 New features and product updates</li>
                        <li>📚 Best practices and tutorials</li>
                        <li>💡 Industry insights and case studies</li>
                    </ul>
                    <p>We're building something special, and we're glad you're part of the journey!</p>
                    <p style="text-align: center;">
                        <a href="{frontend_base_url}" class="button">Explore Firecrawl Agent</a>
                    </p>
                    <p>If you have any questions or feedback, feel free to reach out to us.</p>
                    <p>Best regards,<br><strong>The Firecrawl Agent Team</strong></p>
                </div>
                <div class="footer">
                    <p>You're receiving this email because you subscribed to our newsletter.</p>
                    <p>© 2025 Firecrawl Agentic Pipeline. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        plain_body = f"""
Welcome to Firecrawl Agent!

Thank you for subscribing to our newsletter! We're excited to have you on board.

You'll now receive the latest updates on:
- Agentic RAG and AI search innovations
- New features and product updates
- Best practices and tutorials
- Industry insights and case studies

We're building something special, and we're glad you're part of the journey!

Explore Firecrawl Agent: {frontend_base_url}

If you have any questions or feedback, feel free to reach out to us.

Best regards,
The Firecrawl Agent Team

---
You're receiving this email because you subscribed to our newsletter.
© 2025 Firecrawl Agentic Pipeline. All rights reserved.
        """
        
        # Send email via SendGrid
        success = await email_adapter.send_email(
            to=request.email,
            subject=subject,
            body=plain_body,
            html=html_body
        )
        
        if success:
            return {
                "success": True,
                "message": "Thank you for subscribing! Check your email for a welcome message."
            }
        else:
            return {
                "success": False,
                "message": "Failed to send welcome email. Please try again later."
            }
            
    except Exception as e:
        print(f"Newsletter subscription error: {str(e)}")
        return {
            "success": False,
            "message": "An error occurred. Please try again later."
        }
    
app.include_router(auth_router)
app.include_router(payments_router)
app.include_router(compat_router)

if __name__ == "__main__":
    import uvicorn
    # When running directly, pass app object (reload disabled for direct execution)
    # For reload, use: uvicorn.run("main:app", ...) from project root
    # Disable uvloop to avoid conflicts with nest_asyncio (if imported elsewhere)
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False,  # Disable reload when running directly
        loop="asyncio"  # Use standard asyncio instead of uvloop
    )

