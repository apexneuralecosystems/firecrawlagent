# Execution Guide - FireCrawl Agent RAG Application

This guide explains how to run the FireCrawl Agent application in various ways.

## 🚀 Quick Start

The easiest way to run the application:

```bash
python main.py
```

Or simply double-click `run_app.bat` on Windows.

## 📋 Prerequisites

Before running, ensure you have:

1. **Python 3.11 or later** installed
2. **All dependencies** installed (see Installation)
3. **API Keys** configured (see Configuration)

## 🔧 Installation

### Option 1: Using pip
```bash
pip install -r requirements.txt
```

### Option 2: Using uv (recommended)
```bash
uv sync
```

## ⚙️ Configuration

### 1. Create a `.env` file

Create a `.env` file in the project root with your API keys:

```env
FIRECRAWL_API_KEY=your_firecrawl_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### 2. Get API Keys

- **FireCrawl**: Visit [https://firecrawl.dev/](https://firecrawl.dev/) and sign up
- **OpenRouter**: Visit [https://openrouter.ai/](https://openrouter.ai/) and sign up

## 🎯 Running the Application

### Method 1: Using main.py (Recommended)

This is the recommended way as it includes automatic checks:

```bash
# Run with default settings
python main.py

# Run on custom port
python main.py --port 8080

# Run on custom host and port
python main.py --host 0.0.0.0 --port 8080

# Check setup without running
python main.py --check-only

# Skip checks (not recommended)
python main.py --skip-checks
```

### Method 2: Using Streamlit directly

```bash
streamlit run app.py
```

### Method 3: Using helper scripts

**Windows (Batch):**
```cmd
run_app.bat
```

**Windows (PowerShell):**
```powershell
.\run_app.ps1
```

### Method 4: Package-style execution

```bash
python -m firecrawlagnet
```

## 🔍 Setup Verification

Before running, verify your setup:

```bash
python setup_check.py
```

This will check:
- ✅ Python version compatibility
- ✅ All required dependencies
- ✅ Environment variables
- ✅ Required directories
- ⚪ Optional dependencies

## 📝 Command-Line Options

### main.py options:

```
--port PORT          Port to run the Streamlit app on (default: 8501)
--host HOST          Host to bind the server to (default: localhost)
--check-only         Only perform setup checks, don't run the app
--skip-checks        Skip environment and dependency checks (not recommended)
```

### Examples:

```bash
# Development server (localhost only)
python main.py

# Production server (accessible from network)
python main.py --host 0.0.0.0 --port 8080

# Check setup before running
python main.py --check-only
```

## 🐛 Troubleshooting

### Issue: "Python is not installed"
**Solution:** Install Python 3.11+ from [python.org](https://www.python.org/)

### Issue: "Streamlit not found"
**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

### Issue: "API key errors"
**Solution:** Create a `.env` file with your API keys (see Configuration section)

### Issue: "Port already in use"
**Solution:** Use a different port:
```bash
python main.py --port 8502
```

### Issue: "Module not found"
**Solution:** Install missing dependencies:
```bash
pip install -r requirements.txt
```

## 📦 Project Structure

```
firecrawlagnet/
├── main.py              # Main entry point (USE THIS)
├── app.py               # Streamlit application
├── workflow.py          # Corrective RAG workflow
├── agentic_workflow.py  # Agentic RAG workflow
├── setup_check.py       # Setup verification script
├── run_app.bat          # Windows batch launcher
├── run_app.ps1          # PowerShell launcher
├── requirements.txt     # Python dependencies
├── pyproject.toml       # Project configuration
└── .env                 # Environment variables (create this)
```

## 🎓 Usage Workflow

1. **Setup**: Install dependencies and configure API keys
2. **Verify**: Run `python setup_check.py` to verify setup
3. **Launch**: Run `python main.py` to start the application
4. **Access**: Open browser to `http://localhost:8501`
5. **Upload**: Upload a PDF document in the sidebar
6. **Chat**: Ask questions about your document

## 🔒 Security Notes

- Never commit your `.env` file to version control
- Keep your API keys secure
- Use `localhost` for local development
- Use `0.0.0.0` only when necessary for network access

## 📚 Additional Resources

- [Full README](README.md) - Complete project documentation
- [Setup Instructions](SETUP.md) - Detailed setup guide
- [API Documentation](https://docs.firecrawl.dev/) - FireCrawl API docs

## 💡 Tips

- Use `--check-only` before running to verify setup
- Check the console output for helpful error messages
- The app validates configuration on startup
- Use Ctrl+C to gracefully stop the server

## 🆘 Getting Help

If you encounter issues:

1. Run `python setup_check.py` to diagnose problems
2. Check the error messages in the console
3. Verify your `.env` file configuration
4. Ensure all dependencies are installed
5. Check the [Troubleshooting](#-troubleshooting) section above





