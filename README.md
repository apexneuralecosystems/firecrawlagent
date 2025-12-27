# FireCrawl Agentic RAG Workflow

<div align="center">

![FireCrawl Agent](assets/firecrawl_logo.png)

**An intelligent RAG (Retrieval-Augmented Generation) system combining document retrieval with web search capabilities**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.116+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.2+-61dafb.svg)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.2+-3178c6.svg)](https://www.typescriptlang.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Development](#development)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

FireCrawl Agentic RAG Workflow is a full-stack application that implements an intelligent RAG system using FireCrawl for web search capabilities and LlamaIndex for document processing. The system combines document retrieval with web search to provide comprehensive and accurate answers to user queries.

### Key Capabilities

- **Document Intelligence**: Upload and process PDF documents with intelligent indexing
- **Agentic RAG Workflow**: Advanced agent-based workflow combining document retrieval with web search
- **Real-time Web Search**: FireCrawl integration for enhanced information retrieval
- **Multiple LLM Support**: Compatible with OpenAI, Ollama, LMStudio, OpenRouter, and other providers via LiteLLM
- **Vector Storage**: Supports multiple vector stores (Milvus, Qdrant, ChromaDB)
- **User Authentication**: Complete authentication system with JWT tokens
- **Payment Integration**: PayPal integration for subscription management
- **Modern UI**: Beautiful React frontend with TailwindCSS

## ✨ Features

### Core Features
- ✅ **Document Upload & Processing**: Upload PDF documents for intelligent indexing
- ✅ **Agentic RAG Workflow**: Advanced agent-based workflow that combines document retrieval with web search
- ✅ **FireCrawl Integration**: Real-time web search capabilities for enhanced information retrieval
- ✅ **Session Management**: Track and manage multiple document sessions
- ✅ **Relevance Filtering**: Intelligent filtering of retrieved documents for better accuracy
- ✅ **Chat Interface**: Real-time chat interface for querying documents

### User Features
- ✅ **User Authentication**: Sign up, login, password reset functionality
- ✅ **Protected Routes**: Secure access to dashboard and features
- ✅ **Newsletter Subscription**: Email subscription with SendGrid integration
- ✅ **Payment Processing**: PayPal integration for subscriptions
- ✅ **Responsive Design**: Mobile-friendly interface with dark mode support

### Developer Features
- ✅ **Multiple UI Options**: React frontend, FastAPI backend, and original Streamlit interface
- ✅ **Hot Reload**: Development mode with automatic reloading
- ✅ **API Documentation**: Interactive Swagger UI and ReDoc
- ✅ **Type Safety**: Full TypeScript support in frontend
- ✅ **Database Migrations**: Alembic for database schema management

## 🏗️ Architecture

```
┌─────────────────┐
│   React Frontend │
│   (TypeScript)   │
└────────┬─────────┘
         │ HTTP/REST
         ▼
┌─────────────────┐
│  FastAPI Backend │
│   (Python 3.11+) │
└────────┬─────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐ ┌──────────┐
│ChromaDB│ │ FireCrawl│
│Vector  │ │   API    │
│Store   │ │          │
└────────┘ └──────────┘
    │
    ▼
┌─────────────┐
│  LlamaIndex │
│    RAG      │
│  Workflow   │
└─────────────┘
```

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework for REST API
- **LlamaIndex** - Core RAG framework for document processing and retrieval
- **FireCrawl** - Web scraping and search API for real-time information
- **SQLAlchemy** - Database ORM for session and document management
- **Alembic** - Database migration tool
- **Uvicorn** - ASGI server
- **Apex** - Authentication and payment infrastructure
- **SendGrid** - Email service for notifications

### Frontend
- **React 18** - Modern UI framework
- **TypeScript** - Type-safe development
- **TailwindCSS** - Utility-first CSS framework
- **Vite** - Fast build tool and dev server
- **Axios** - HTTP client for API communication
- **React Router** - Client-side routing
- **Framer Motion** - Animation library
- **Lucide React** - Icon library

### Core Libraries
- **LlamaIndex** - Document processing and RAG workflows
- **LiteLLM** - Unified LLM interface supporting multiple providers
- **Vector Stores**: Milvus, Qdrant, ChromaDB support
- **Streamlit** - Original web interface (still available)

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11 or later** - [Download Python](https://www.python.org/downloads/)
- **Node.js 18+ or Bun** - [Download Node.js](https://nodejs.org/) or [Install Bun](https://bun.sh/)
- **FireCrawl API Key** - [Get your API key](https://firecrawl.dev/)
- **LLM API Key** - Choose one:
  - **OpenRouter** (Recommended) - [Get API key](https://openrouter.ai/)
  - **OpenAI** - [Get API key](https://platform.openai.com/)
  - **Ollama** - Local models (no API key needed)
  - **LMStudio** - Local models (no API key needed)

### Optional Prerequisites
- **PostgreSQL** - For production database (SQLite used by default)
- **SendGrid API Key** - For email functionality
- **PayPal API Credentials** - For payment processing

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd firecrawlagent
```

### 2. Set Up Environment Variables
```bash
cp .envexample .env
```

Edit `.env` and add your API keys:
```env
FIRECRAWL_API_KEY=your_firecrawl_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
LLM_MODEL=openrouter/google/gemini-2.0-flash-exp:free

# Optional: Email and Payment
SENDGRID_API_KEY=your_sendgrid_api_key
PAYPAL_CLIENT_ID=your_paypal_client_id
PAYPAL_CLIENT_SECRET=your_paypal_client_secret
FRONTEND_BASE_URL=http://localhost:3000
```

### 3. Install Dependencies

**Backend:**
```bash
pip install -r requirements.txt
# Or using uv (recommended):
uv sync
```

**Frontend:**
```bash
cd frontend
bun install
# Or using npm:
npm install
```

### 4. Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
python main.py
# Or: uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
bun run dev
# Or: npm run dev
```

### 5. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📥 Installation

### Detailed Installation Steps

#### Backend Installation

1. **Create Virtual Environment** (Recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install Python Dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set Up Database** (if using Alembic):
```bash
cd backend
alembic upgrade head
```

#### Frontend Installation

1. **Install Node Dependencies**:
```bash
cd frontend
bun install  # Or: npm install
```

2. **Create Frontend Environment File** (Optional):
```bash
echo "VITE_API_URL=http://localhost:8000" > .env
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Required
FIRECRAWL_API_KEY=your_firecrawl_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
SECRET_KEY=your-secret-key-minimum-32-characters-long

# Runtime (set to production in deploy)
ENV=development

# CORS (required in production; comma-separated)
ALLOWED_ORIGINS=http://localhost:3000

# Optional - LLM Configuration
LLM_MODEL=openrouter/google/gemini-2.0-flash-exp:free

# Optional - Email Service
SENDGRID_API_KEY=your_sendgrid_api_key

# Optional - Payment Processing
PAYPAL_CLIENT_ID=your_paypal_client_id
PAYPAL_CLIENT_SECRET=your_paypal_client_secret
PAYPAL_MODE=sandbox  # or 'live'

# Optional - Frontend URL
FRONTEND_BASE_URL=http://localhost:3000

# Optional - Database (defaults to SQLite)
DATABASE_URL=sqlite:///./app.db
# For PostgreSQL: DATABASE_URL=postgresql://user:password@localhost/dbname

# Optional - Chroma persistence path (use a persistent volume in production)
CHROMA_DB_PATH=./chroma_db
```

### LLM Configuration

The system supports various LLM providers:

- **OpenRouter** (Recommended): Supports multiple models including free tiers
- **OpenAI**: GPT-3.5, GPT-4, and other OpenAI models
- **Ollama**: Local models - no API key needed
- **LMStudio**: Local models - no API key needed

Set the model in your `.env`:
```env
LLM_MODEL=openrouter/google/gemini-2.0-flash-exp:free
```

### Vector Store Configuration

The system supports multiple vector stores:
- **ChromaDB** (Default): Local file-based storage
- **Milvus**: Distributed vector database
- **Qdrant**: High-performance vector database

## 🏃 Running the Application

### Option 1: Full-Stack Application (Recommended)

Run both backend and frontend:

**Terminal 1 - Backend:**
```bash
cd backend
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
bun run dev
```

### Option 2: Backend Only (API)

Run just the FastAPI backend:
```bash
cd backend
python main.py
# Or from project root:
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Access the API at `http://localhost:8000` and view docs at `http://localhost:8000/docs`

### Option 3: Streamlit Interface

Run the original Streamlit app:
```bash
python main.py
# Or: streamlit run app.py
```

### Option 4: Production Deployment

**Backend:**
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1
# Or with Gunicorn:
gunicorn main:app -w 1 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**Frontend:**
```bash
cd frontend
bun run build
# Serve the dist/ directory with a web server like nginx
```

#### Production notes
- **Single worker required (currently)**: the backend stores active RAG workflows in-memory, so use `--workers 1`.
- **CORS**: set `ALLOWED_ORIGINS` in production (API fails fast if missing).
- **Chroma persistence**: set `CHROMA_DB_PATH` to a persistent volume path.
- **Email**: SendGrid requires outbound HTTPS with valid certificate trust (configure `SSL_CERT_FILE` on your host if needed).

### Option 5: Setup Verification

Before running, verify your setup:
```bash
python setup_check.py
```

## 📁 Project Structure

```
firecrawlagent/
├── backend/                    # FastAPI backend
│   ├── main.py                # FastAPI application entry point
│   ├── app/
│   │   ├── services/         # Business logic
│   │   │   └── workflow_service.py
│   │   ├── routers/          # API route handlers
│   │   │   ├── auth.py       # Authentication routes
│   │   │   └── payments.py    # Payment routes
│   │   ├── models/           # Database models
│   │   │   ├── session.py
│   │   │   ├── document.py
│   │   │   ├── chat_message.py
│   │   │   ├── user.py
│   │   │   ├── organization.py
│   │   │   ├── payment.py
│   │   │   └── workflow.py
│   │   ├── deps/             # Dependencies
│   │   │   └── auth.py       # Auth dependencies
│   │   ├── auth/             # Authentication utilities
│   │   │   └── jwt.py
│   │   ├── database.py       # Database configuration
│   │   └── apex_client.py    # Apex client initialization
│   ├── alembic/              # Database migrations
│   ├── requirements.txt      # Backend dependencies
│   ├── run.sh                # Production startup script
│   ├── run_dev.sh            # Development script
│   └── README.md             # Backend documentation
│
├── frontend/                  # React frontend
│   ├── src/
│   │   ├── components/       # React components
│   │   │   ├── ChatInterface.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   ├── WelcomeScreen.tsx
│   │   │   ├── MessageBubble.tsx
│   │   │   ├── ProcessDetails.tsx
│   │   │   ├── AuthLayout.tsx
│   │   │   ├── DashboardLayout.tsx
│   │   │   ├── ProtectedRoute.tsx
│   │   │   └── PaymentComponent.tsx
│   │   ├── pages/           # Page components
│   │   │   ├── LandingPage.tsx
│   │   │   ├── LoginPage.tsx
│   │   │   ├── SignupPage.tsx
│   │   │   ├── ForgotPasswordPage.tsx
│   │   │   └── PaymentPage.tsx
│   │   ├── services/         # API services
│   │   │   └── api.ts
│   │   ├── context/          # React context
│   │   │   └── AuthContext.tsx
│   │   ├── App.tsx           # Main app component
│   │   ├── main.tsx          # Entry point
│   │   └── index.css         # Global styles
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   ├── vite.config.ts
│   └── README.md             # Frontend documentation
│
├── app.py                     # Streamlit application (original)
├── agentic_workflow.py        # Agentic RAG workflow implementation
├── main.py                    # Entry point for Streamlit app
├── langchain_patch.py         # LangChain compatibility patches
├── pydantic_config.py         # Pydantic configuration
├── setup_check.py             # Setup verification script
├── pyproject.toml             # Project dependencies (uv)
├── requirements.txt            # Python package requirements
├── API_DOCUMENTATION.md        # API endpoint documentation
├── assets/                     # Images and animations
└── README.md                   # This file
```

## 📚 API Documentation

### Interactive Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

#### Health Check
- `GET /` - Basic health check
- `GET /api/health` - Detailed health check

#### Document Management
- `POST /api/upload` - Upload and process PDF document
- `GET /api/sessions` - List all active sessions
- `GET /api/sessions/{session_id}` - Get session information
- `DELETE /api/sessions/{session_id}` - Delete a session

#### Chat
- `POST /api/chat` - Send a chat message

#### Authentication
- `POST /api/auth/signup` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Refresh access token
- `POST /api/auth/forgot-password` - Request password reset
- `POST /api/auth/reset-password` - Reset password with token
- `POST /api/auth/change-password` - Change password
- `GET /api/auth/me` - Get current user info

#### Payments
- `GET /api/payments/config` - Check PayPal configuration
- `POST /api/payments/create-order` - Create PayPal order
- `POST /api/payments/capture-order` - Capture PayPal order

#### Newsletter
- `POST /api/newsletter/subscribe` - Subscribe to newsletter

For detailed API documentation, see [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

## 🔧 Development

### Backend Development

```bash
cd backend
# Install dependencies
pip install -r requirements.txt

# Run with hot reload
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# Run database migrations
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "description"
```

### Frontend Development

```bash
cd frontend
# Install dependencies
bun install

# Run development server
bun run dev

# Build for production
bun run build

# Preview production build
bun run preview
```

### Code Quality

**Python:**
```bash
# Format code
black .
isort .

# Type checking (if using mypy)
mypy backend/
```

**TypeScript:**
```bash
cd frontend
# Lint
bun run lint

# Type check
tsc --noEmit
```

### Testing

- **Backend API**: Test endpoints using the Swagger UI at `http://localhost:8000/docs`
- **Frontend**: Hot reload enabled during development
- **Streamlit**: Use `python main.py` for the original interface

## 🐛 Troubleshooting

### Common Issues

1. **API Key Errors**
   - Ensure your FireCrawl and LLM API keys are correctly set in `.env`
   - Verify the keys are active and have sufficient credits

2. **Import Errors**
   - Make sure you're using Python 3.11 or later
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check that virtual environment is activated

3. **Database Issues**
   - Clear storage directories if experiencing database corruption
   - Run migrations: `cd backend && alembic upgrade head`
   - Check database file permissions

4. **Memory Issues**
   - Large documents may require more memory
   - Consider document chunking for very large files
   - Increase system memory or use smaller documents

5. **Timeout Errors**
   - Increase timeout settings for complex queries
   - Check network connectivity
   - Verify API service availability

6. **CORS Errors**
   - Ensure backend CORS settings allow your frontend origin
   - Check that `FRONTEND_BASE_URL` matches your frontend URL

7. **Port Already in Use**
   - Change port in backend: `uvicorn backend.main:app --port 8001`
   - Change port in frontend: Update `vite.config.ts` or use `bun run dev --port 3001`

### Debug Mode

Enable debug logging in the workflow:
```python
workflow = AgenticRAGWorkflow(
    index=index,
    firecrawl_api_key=api_key,
    verbose=True,  # Enable debug logging
    llm=llm
)
```

### Getting Help

- Check the [TROUBLESHOOTING.md](backend/TROUBLESHOOTING.md) file
- Review API documentation at `http://localhost:8000/docs`
- Check logs in the terminal for detailed error messages

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

### Contribution Guidelines

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style

- **Python**: Follow PEP 8, use Black for formatting
- **TypeScript**: Follow ESLint rules, use Prettier for formatting
- **Commits**: Use clear, descriptive commit messages

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [LlamaIndex](https://github.com/run-llama/llama_index) for the RAG framework
- [FireCrawl](https://firecrawl.dev/) for web scraping capabilities
- [FastAPI](https://fastapi.tiangolo.com/) for the modern backend framework
- [React](https://react.dev/) for the frontend framework
- [Streamlit](https://streamlit.io/) for the original web interface
- [Milvus](https://milvus.io/), [Qdrant](https://qdrant.tech/), [ChromaDB](https://www.trychroma.com/) for vector storage
- [Apex](https://github.com/apex-ai/apex) for authentication and payment infrastructure

## 📞 Support

For support, please open an issue on GitHub or contact the development team.

---

<div align="center">

**Built with ❤️ using FireCrawl, LlamaIndex, FastAPI, and React**

[Documentation](./README.md) • [API Docs](./API_DOCUMENTATION.md) • [Backend README](./backend/README.md) • [Frontend README](./frontend/README.md)

</div>
