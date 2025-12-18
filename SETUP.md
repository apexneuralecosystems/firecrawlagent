# Setup Instructions

## Quick Start

1. **Create a `.env` file** in the project root with your API keys:
   ```
   FIRECRAWL_API_KEY=your_firecrawl_api_key_here
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   ```

2. **Get API Keys:**
   - FireCrawl: Visit https://firecrawl.dev/ and sign up
   - OpenRouter: Visit https://openrouter.ai/ and sign up

3. **Run the application:**
   
   **Option 1 - Using helper script (Windows):**
   - Double-click `run_app.bat` or run `.\run_app.ps1` in PowerShell
   
   **Option 2 - Using Python directly:**
   ```bash
   python -m streamlit run app.py
   ```
   
   **Note for Windows:** If `streamlit` command is not recognized, use `python -m streamlit run app.py` instead.

## What Was Fixed

- ✅ Updated Pydantic v1 `class Config` to Pydantic v2 `model_config` in Event classes
- ✅ Verified all imports are working correctly
- ✅ Tested workflow initialization
- ✅ All dependencies are properly installed

## Troubleshooting

If you encounter any issues:

1. **API Key Errors**: Make sure your `.env` file is in the project root and contains both API keys
2. **Import Errors**: Run `pip install -r requirements.txt` to ensure all dependencies are installed
3. **Streamlit Issues**: Make sure you're running with `streamlit run app.py` not `python app.py`

