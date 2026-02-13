# FireCrawl Agent Backend API

<div align="center">

**FastAPI backend for the FireCrawl Agent RAG Application**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.116+-green.svg)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Uvicorn](https://img.shields.io/badge/Uvicorn-0.35+-brightgreen.svg)](https://www.uvicorn.org/)

</div>

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Quick Start](#-quick-start)
- [Installation (Detailed)](#-installation-detailed)
- [Configuration](#configuration)
- [Running the Server](#running-the-server)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Database](#database)
- [Authentication](#authentication)
- [Development](#development)
- [Testing](#testing)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Complete Commands Reference](#-complete-commands-reference)

## 🎯 Overview

The FireCrawl Agent Backend is a FastAPI-based REST API that powers the FireCrawl Agentic RAG Workflow application. It provides endpoints for document processing, chat interactions, user authentication, payment processing, and session management.

### Key Responsibilities

- **Document Processing**: Upload, process, and index PDF documents using LlamaIndex
- **RAG Workflow**: Execute agentic RAG workflows combining document retrieval with web search
- **Session Management**: Track and manage user sessions and document contexts
- **User Authentication**: JWT-based authentication with Apex framework
- **Payment Processing**: PayPal integration for subscription management
- **Email Services**: SendGrid integration for transactional emails

## ✨ Features

- ✅ **RESTful API**: Modern FastAPI-based REST API with automatic OpenAPI documentation
- ✅ **Document Upload**: Secure PDF document upload and processing
- ✅ **Agentic RAG**: Advanced agent-based RAG workflow execution
- ✅ **Session Management**: In-memory session storage (Redis-ready for production)
- ✅ **User Authentication**: Complete auth system with JWT tokens
- ✅ **Password Management**: Forgot password, reset password, change password
- ✅ **Payment Integration**: PayPal order creation and capture
- ✅ **Newsletter Subscription**: Email subscription with SendGrid
- ✅ **CORS Support**: Configured for frontend integration
- ✅ **Health Checks**: Comprehensive health check endpoints
- ✅ **Database Models**: SQLAlchemy models for users, sessions, documents, payments
- ✅ **Database Migrations**: Alembic for schema management

## 🛠️ Tech Stack

### Core Framework
- **FastAPI 0.116+** - Modern Python web framework
- **Uvicorn** - ASGI server with hot reload support
- **Python 3.11+** - Runtime environment

### Key Libraries
- **LlamaIndex** - RAG framework for document processing
- **SQLAlchemy** - Database ORM
- **Alembic** - Database migration tool
- **Apex** - Authentication and payment infrastructure
- **SendGrid** - Email service integration
- **Pydantic** - Data validation and settings management
- **python-multipart** - File upload support
- **python-dotenv** - Environment variable management

### Database
- **SQLite** - Default database (development)
- **PostgreSQL** - Production database (via asyncpg/psycopg2)

## 📦 Prerequisites

- Python 3.11 or later (Python 3.13 supported)
- pip or uv package manager
- Node.js & npm (for PM2 process manager - optional)
- PostgreSQL (for production database)
- FireCrawl API key
- LLM API key (OpenRouter, OpenAI, etc.)
- (Optional) SendGrid API key for emails
- (Optional) PayPal credentials for payments

---

## ⚡ Quick Start

```bash
# 1. Navigate to backend directory
cd backend

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies (IMPORTANT: Install in this order!)
pip install -r ../requirements.txt   # Root-level requirements FIRST
pip install -r requirements.txt      # Backend-specific requirements
pip install email-validator          # Required for Pydantic email validation

# 4. Run database migrations
alembic upgrade head

# 5. Start the server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

---

## 🚀 Installation (Detailed)

### Step 1: Navigate to Backend Directory

```bash
cd /path/to/firecrawlagent/backend
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate     # On Windows
```

### Step 3: Install Dependencies

> ⚠️ **IMPORTANT**: You must install dependencies in the correct order!

**Step 3a: Install Root-Level Requirements (FIRST)**

The root `requirements.txt` contains all the core dependencies including LlamaIndex, ChromaDB, LiteLLM, and other essential packages:

```bash
pip install -r ../requirements.txt
```

This will install 150+ packages including:
- `llama-index` - RAG framework
- `chromadb` - Vector database
- `litellm` - LLM integration
- `firecrawl-py` - Web scraping
- `openai` - OpenAI client
- And many more...

**Step 3b: Install Backend-Specific Requirements**

```bash
pip install -r requirements.txt
```

This installs FastAPI server dependencies:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `python-multipart` - File uploads
- `asyncpg` / `psycopg2-binary` - PostgreSQL drivers

**Step 3c: Install Additional Required Packages**

```bash
# Required for Pydantic email validation
pip install email-validator

# Install Apex SaaS Framework (for authentication)
pip install apex-saas-framework
```

### Step 4: Set Up Environment Variables

Create a `.env` file in the backend directory:

```bash
cp ../.env .env  # Copy from parent if exists
# OR create new one
touch .env
```

Add the following configuration:

```env
# ═══════════════════════════════════════════════════════════════
# REQUIRED CONFIGURATION
# ═══════════════════════════════════════════════════════════════

# FireCrawl API Key (get from https://firecrawl.dev)
FIRECRAWL_API_KEY=your_firecrawl_api_key_here

# LLM API Key (OpenRouter recommended)
OPENROUTER_API_KEY=your_openrouter_api_key_here

# ═══════════════════════════════════════════════════════════════
# DATABASE CONFIGURATION
# ═══════════════════════════════════════════════════════════════

# SQLite (Development)
DATABASE_URL=sqlite:///./app.db

# PostgreSQL (Production) - Choose one format:
# DATABASE_URL=postgresql://user:password@localhost:5432/dbname
# DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname

# ═══════════════════════════════════════════════════════════════
# OPTIONAL CONFIGURATION
# ═══════════════════════════════════════════════════════════════

# LLM Model (default: gemini-2.0-flash)
LLM_MODEL=openrouter/openai/gpt-4o-mini

# Email Service (SendGrid)
SENDGRID_API_KEY=your_sendgrid_api_key

# Payment Processing (PayPal)
PAYPAL_CLIENT_ID=your_paypal_client_id
PAYPAL_CLIENT_SECRET=your_paypal_client_secret
PAYPAL_MODE=sandbox  # or 'live'

# Frontend URL (for email links)
FRONTEND_BASE_URL=http://localhost:3000

# JWT Secret (REQUIRED for production)
SECRET_KEY=your_super_secret_key_here

# CORS Origins (REQUIRED for production)
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Step 5: Set Up Database

**Run Migrations:**
```bash
alembic upgrade head
```

**Create New Migration (when models change):**
```bash
alembic revision --autogenerate -m "description of changes"
alembic upgrade head
```

**Rollback Migration:**
```bash
alembic downgrade -1
```

## ⚙️ Configuration

### Environment Variables

The backend reads configuration from environment variables. Key variables:

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `FIRECRAWL_API_KEY` | Yes | FireCrawl API key for web search | - |
| `OPENROUTER_API_KEY` | Yes | OpenRouter API key for LLM | - |
| `LLM_MODEL` | No | LLM model identifier | `openrouter/openai/gpt-4o-mini` |
| `DATABASE_URL` | No | Database connection string | `sqlite:///./app.db` |
| `SENDGRID_API_KEY` | No | SendGrid API key for emails | - |
| `PAYPAL_CLIENT_ID` | No | PayPal client ID | - |
| `PAYPAL_CLIENT_SECRET` | No | PayPal client secret | - |
| `PAYPAL_MODE` | No | PayPal mode (sandbox/live) | `sandbox` |
| `ENV` / `ENVIRONMENT` | No | Runtime environment (`development`/`production`) | `development` |
| `SECRET_KEY` | **Yes (prod)** | JWT signing secret (must be strong + stable) | - |
| `ALLOWED_ORIGINS` | **Yes (prod)** | Comma-separated CORS origins | - |
| `CHROMA_DB_PATH` | No | Chroma persistence path | `./chroma_db` |
| `REQUIRE_SINGLE_WORKER` | No | Enforce single worker in production (`1`/`0`) | `1` |
| `SSL_CERT_FILE` | No | CA bundle path for outbound HTTPS (SendGrid) | OS default |
| `FRONTEND_BASE_URL` | No | Frontend base URL (emails/links) | `http://localhost:3000` |

### CORS Configuration

CORS is configured via the `ALLOWED_ORIGINS` environment variable.

- **Development**: if `ALLOWED_ORIGINS` is not set, the API allows `*`
- **Production**: the API **fails fast** if `ALLOWED_ORIGINS` is not set

Example:

```env
ALLOWED_ORIGINS=https://app.yourdomain.com,https://www.yourdomain.com
```

## 🏃 Running the Server

### Development Mode

> ⚠️ **IMPORTANT**: Always run commands from the `backend` directory with the virtual environment activated!

**Option 1: Direct uvicorn command (Recommended)**
```bash
# Make sure you're in the backend directory
cd /path/to/firecrawlagent/backend

# Activate virtual environment
source venv/bin/activate

# Run the server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Option 2: Using the development script**
```bash
./run_dev.sh
```

**Option 3: Using Python directly**
```bash
python main.py
```

The API will be available at:
- **API**: `http://localhost:8000`
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

### Production Mode

**IMPORTANT**: This backend stores active RAG workflows in-memory. Run a **SINGLE worker** only!

**Option 1: Using uvicorn**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1
```

**Option 2: Using Gunicorn**
```bash
gunicorn main:app -w 1 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**Option 3: Using the production script**
```bash
./run.sh
```

---

### Using PM2 (Process Manager)

PM2 keeps your server running in the background and auto-restarts on crashes.

**Step 1: Install PM2 globally**
```bash
npm install -g pm2
```

**Step 2: Create ecosystem file**

Create `ecosystem.config.js` in the backend directory:

```javascript
module.exports = {
  apps: [{
    name: "firecrawl-api",
    cwd: "/path/to/firecrawlagent/backend",
    script: "venv/bin/uvicorn",
    args: "main:app --host 0.0.0.0 --port 8000",
    interpreter: "none",
    env: {
      PATH: "./venv/bin:" + process.env.PATH
    }
  }]
};
```

**Step 3: Start with PM2**
```bash
pm2 start ecosystem.config.js
```

**Alternative: One-liner command**
```bash
cd /path/to/firecrawlagent/backend
pm2 start "source venv/bin/activate && uvicorn main:app --host 0.0.0.0 --port 8000" --name firecrawl-api --interpreter bash
```

**PM2 Commands Reference:**

| Command | Description |
|---------|-------------|
| `pm2 list` | Show all running processes |
| `pm2 logs firecrawl-api` | View logs |
| `pm2 restart firecrawl-api` | Restart server |
| `pm2 stop firecrawl-api` | Stop server |
| `pm2 delete firecrawl-api` | Remove from PM2 |
| `pm2 save` | Save process list |
| `pm2 startup` | Enable auto-start on boot |

## 📡 API Endpoints

### Health Check

- **GET** `/` - Basic health check
  - Response: `{"message": "FireCrawl Agent API", "status": "running", "version": "1.0.0"}`

- **GET** `/api/health` - Detailed health check
  - Response: Includes session count and environment status

### Document Management

- **POST** `/api/upload` - Upload and process PDF document
  - Request: Multipart form data with `file` field
  - Response: `{"session_id": "uuid", "filename": "name.pdf", "status": "processed", "uploaded_at": "timestamp"}`

- **GET** `/api/sessions` - List all active sessions
  - Response: `{"sessions": [...], "count": int}`

- **GET** `/api/sessions/{session_id}` - Get session information
  - Response: Session object (excluding workflow object)

- **DELETE** `/api/sessions/{session_id}` - Delete a session
  - Response: `{"status": "deleted", "session_id": "uuid"}`

### Chat / Workflow

- **POST** `/api/chat` - Send a chat message
  - Request: `{"session_id": "uuid", "message": "your question"}`
  - Response: `{"response": "agent answer", "session_id": "uuid", "logs": "optional logs"}`

### Authentication

- **POST** `/api/auth/signup` - User registration
  - Request: `{"email": "...", "password": "...", "first_name": "...", "last_name": "...", "username": "..."}`
  - Response: `{"id": "...", "email": "..."}`

- **POST** `/api/auth/login` - User login
  - Request: `{"email": "...", "password": "..."}`
  - Response: Token object (JWT)

- **POST** `/api/auth/refresh` - Refresh access token
  - Request: `{"refresh_token": "..."}`
  - Response: Token object

- **POST** `/api/auth/forgot-password` - Request password reset
  - Request: `{"email": "..."}`
  - Response: `{"ok": true, "reset_token": "..."}`

- **POST** `/api/auth/reset-password` - Reset password with token
  - Request: `{"token": "...", "new_password": "..."}`
  - Response: `{"ok": bool}`

- **POST** `/api/auth/change-password` - Change password
  - Request: `{"user_id": "...", "old_password": "...", "new_password": "..."}`
  - Response: `{"ok": bool}`

- **GET** `/api/auth/me` - Get current user info
  - Requires: Authentication token
  - Response: User object

### Payments

- **GET** `/api/payments/config` - Check PayPal configuration
  - Requires: Authentication
  - Response: Configuration status

- **POST** `/api/payments/create-order` - Create PayPal order
  - Requires: Authentication
  - Request: `{"amount": float, "currency": "USD", "description": "...", ...}`
  - Response: PayPal order object

- **POST** `/api/payments/capture-order` - Capture PayPal order
  - Requires: Authentication
  - Request: `{"order_id": "..."}`
  - Response: Payment confirmation

### Newsletter

- **POST** `/api/newsletter/subscribe` - Subscribe to newsletter
  - Request: `{"email": "..."}`
  - Response: `{"success": bool, "message": "..."}`

### API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 📁 Project Structure

```
backend/
├── main.py                    # FastAPI application entry point
├── app/
│   ├── __init__.py
│   ├── services/             # Business logic
│   │   └── workflow_service.py  # RAG workflow service
│   ├── routers/              # API route handlers
│   │   ├── auth.py           # Authentication routes
│   │   └── payments.py       # Payment routes
│   ├── models/               # Database models
│   │   ├── user.py           # User model
│   │   ├── session.py        # Session model
│   │   ├── document.py       # Document model
│   │   ├── chat_message.py   # Chat message model
│   │   ├── workflow.py       # Workflow model
│   │   ├── organization.py   # Organization model
│   │   └── payment.py        # Payment model
│   ├── deps/                 # Dependencies
│   │   └── auth.py           # Auth dependencies (get_current_user)
│   ├── auth/                 # Authentication utilities
│   │   └── jwt.py            # JWT utilities
│   ├── database.py           # Database configuration
│   └── apex_client.py        # Apex client initialization
├── alembic/                  # Database migrations
│   ├── env.py
│   ├── script.py.mako
│   └── versions/             # Migration files
├── alembic.ini               # Alembic configuration
├── requirements.txt          # Backend dependencies
├── run.sh                    # Production startup script
├── run_dev.sh                # Development script with reload
├── uploads/                  # Uploaded files directory
├── chroma_db/                # ChromaDB vector store
└── README.md                 # This file
```

## 🗄️ Database

### Database Models

The backend uses SQLAlchemy ORM with the following models:

- **User**: User accounts and authentication
- **Session**: Document processing sessions
- **Document**: Uploaded documents metadata
- **ChatMessage**: Chat conversation history
- **Workflow**: Workflow execution records
- **Organization**: Organization/tenant management
- **Payment**: Payment transaction records

### Database Migrations

**Run Migrations:**
```bash
alembic upgrade head
```

**Create New Migration:**
```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
```

**Rollback Migration:**
```bash
alembic downgrade -1
```

**View Migration History:**
```bash
alembic history
```

### Database Connection

The backend supports both SQLite (default) and PostgreSQL:

**SQLite (Development):**
```env
DATABASE_URL=sqlite:///./app.db
```

**PostgreSQL (Production):**
```env
DATABASE_URL=postgresql://user:password@localhost/dbname
# Or async:
DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
```

## 🔐 Authentication

The backend uses JWT-based authentication via the Apex framework.

### Authentication Flow

1. User signs up or logs in via `/api/auth/signup` or `/api/auth/login`
2. Backend returns JWT access token and refresh token
3. Frontend includes token in `Authorization: Bearer <token>` header
4. Protected routes use `get_current_user` dependency to validate token

### Protected Routes

Routes that require authentication use the `get_current_user` dependency:

```python
from app.deps.auth import get_current_user

@router.get("/protected")
def protected_route(user=Depends(get_current_user)):
    return {"user": user}
```

### Token Refresh

Access tokens expire after a set time. Use the refresh token to get a new access token:

```python
POST /api/auth/refresh
{
    "refresh_token": "your_refresh_token"
}
```

## 💻 Development

### Development Setup

1. **Activate Virtual Environment:**
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install Development Dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run with Hot Reload:**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Code Structure

- **Routes**: Define API endpoints in `app/routers/`
- **Services**: Business logic in `app/services/`
- **Models**: Database models in `app/models/`
- **Dependencies**: Shared dependencies in `app/deps/`

### Adding New Endpoints

1. Create or update router in `app/routers/`
2. Import and include router in `main.py`:
```python
from app.routers.your_router import router as your_router
app.include_router(your_router)
```

### Code Quality

**Format Code:**
```bash
black .
isort .
```

**Type Checking:**
```bash
mypy backend/  # If mypy is configured
```

## 🧪 Testing

### Manual Testing

Use the interactive API documentation:
- Visit `http://localhost:8000/docs`
- Test endpoints directly from the Swagger UI

### Testing with curl

**Health Check:**
```bash
curl http://localhost:8000/api/health
```

**Upload Document:**
```bash
curl -X POST "http://localhost:8000/api/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf"
```

**Chat:**
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"session_id": "uuid", "message": "your question"}'
```

## 🚀 Deployment

### Production Considerations

1. **Use PostgreSQL** instead of SQLite
2. **Run a single worker** (until shared session/workflow storage is implemented)
3. **Configure CORS** using `ALLOWED_ORIGINS`
4. **Use environment variables** for all secrets
5. **Enable HTTPS** with SSL certificates
6. **Set up logging** and monitoring
7. **Use process manager** like systemd or supervisor
8. **Configure reverse proxy** (nginx) in front of the application

### Deployment Options

**Option 1: Docker**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Option 2: Cloud Platforms**
- Deploy to platforms like Railway, Render, Fly.io, or AWS
- Configure environment variables
- Set up database connection

**Option 3: Traditional Server**
```bash
# Install dependencies
pip install -r requirements.txt

# Run with Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 🐛 Troubleshooting

### Common Issues

1. **ModuleNotFoundError: No module named 'backend'**
   ```
   ModuleNotFoundError: No module named 'backend'
   ```
   **Solution**: You're running the command from the wrong directory.
   - If inside `backend/` directory, use: `uvicorn main:app --reload`
   - If at project root, use: `uvicorn backend.main:app --reload`

2. **ModuleNotFoundError: No module named 'llama_index'**
   ```
   ModuleNotFoundError: No module named 'llama_index'
   ```
   **Solution**: Install root requirements first:
   ```bash
   pip install -r ../requirements.txt
   ```

3. **ModuleNotFoundError: No module named 'email_validator'**
   ```
   ImportError: email-validator is not installed
   ```
   **Solution**: Install email-validator:
   ```bash
   pip install email-validator
   ```

4. **bcrypt Version Warning**
   ```
   AttributeError: module 'bcrypt' has no attribute '__about__'
   ```
   **Solution**: This is a harmless warning. To fix it:
   ```bash
   pip install bcrypt==4.0.1
   ```

5. **Import Errors**
   - Ensure you're in the backend directory
   - Check that all dependencies are installed
   - Verify virtual environment is activated

6. **Database Connection Errors**
   - Check `DATABASE_URL` environment variable
   - Verify database is running (for PostgreSQL)
   - Check database file permissions (for SQLite)

7. **Port Already in Use**
   - Change port: `uvicorn main:app --port 8001`
   - Kill existing process: `lsof -ti:8000 | xargs kill`

8. **CORS Errors**
   - Verify CORS configuration in `main.py`
   - Check `ALLOWED_ORIGINS` environment variable

9. **Authentication Errors**
   - Verify JWT secret is set
   - Check token expiration
   - Ensure token is included in Authorization header

10. **File Upload Errors**
    - Check file size limits
    - Verify `uploads/` directory exists and is writable
    - Ensure `python-multipart` is installed

### Debug Mode

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Getting Help

- Check logs in terminal for detailed error messages
- Review API documentation at `/docs`
- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for more details

---

## 📋 Complete Commands Reference

### Installation Commands

```bash
# Navigate to backend
cd /path/to/firecrawlagent/backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# Install ALL dependencies (in order)
pip install -r ../requirements.txt    # Root requirements FIRST
pip install -r requirements.txt       # Backend requirements
pip install email-validator           # Email validation
pip install apex-saas-framework       # Authentication framework

# Fix bcrypt warning (optional)
pip install bcrypt==4.0.1
```

### Database Commands

```bash
# Run migrations
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "description"

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history
```

### Server Commands

```bash
# Development (with auto-reload)
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Production (single worker)
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1

# With Gunicorn
gunicorn main:app -w 1 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### PM2 Commands

```bash
# Start server
pm2 start ecosystem.config.js

# View processes
pm2 list

# View logs
pm2 logs firecrawl-api

# Restart
pm2 restart firecrawl-api

# Stop
pm2 stop firecrawl-api

# Delete
pm2 delete firecrawl-api

# Save for auto-restart
pm2 save
pm2 startup
```

### Utility Commands

```bash
# Check installed packages
pip list

# Export requirements
pip freeze > requirements-lock.txt

# Update pip
pip install --upgrade pip

# Kill process on port
lsof -ti:8000 | xargs kill

# Check if server is running
curl http://localhost:8000/api/health
```

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LlamaIndex Documentation](https://docs.llamaindex.ai/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)

---

<div align="center">

**Built with FastAPI, LlamaIndex, and Apex**

[Back to Main README](../README.md) • [API Documentation](../API_DOCUMENTATION.md)

</div>
