# Quick Start Guide

Get up and running with FireCrawl Agent in 3 simple steps!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

Or with uv:
```bash
uv sync
```

## Step 2: Configure API Keys

Create a `.env` file in the project root:

```env
FIRECRAWL_API_KEY=your_firecrawl_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

Get your API keys:
- FireCrawl: https://firecrawl.dev/
- OpenRouter: https://openrouter.ai/

## Step 3: Run the Application

**Easiest way:**
```bash
python main.py
```

**Or use helper scripts:**
- Windows: Double-click `run_app.bat`
- Unix/Linux/Mac: `./run_app.sh` (you may need to run `chmod +x run_app.sh` first)

**Or verify setup first:**
```bash
python setup_check.py
python main.py
```

That's it! The app will open in your browser at `http://localhost:8501`

## What's Next?

1. Upload a PDF document in the sidebar
2. Ask questions about your document
3. The AI will search the document and web to answer your questions

## Need Help?

- See [EXECUTION_GUIDE.md](EXECUTION_GUIDE.md) for detailed instructions
- See [SETUP.md](SETUP.md) for troubleshooting
- Run `python setup_check.py` to diagnose issues





