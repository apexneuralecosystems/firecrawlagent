@echo off
REM FireCrawl Agent RAG Application Launcher
REM This script checks prerequisites and starts the application

echo ============================================================
echo   FireCrawl Agent RAG Application
echo ============================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.11 or later and try again.
    pause
    exit /b 1
)

echo [INFO] Python found
echo.

REM Check if main.py exists (preferred method)
if exist main.py (
    echo [INFO] Starting application using main.py...
    echo.
    python main.py %*
    if errorlevel 1 (
        echo.
        echo [ERROR] Failed to start application
        pause
        exit /b 1
    )
) else (
    REM Fallback to direct streamlit command
    echo [INFO] Starting application using streamlit directly...
    echo.
    
    REM Check if streamlit is available
    python -m streamlit --version >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Streamlit is not installed
        echo Please install dependencies: pip install -r requirements.txt
        pause
        exit /b 1
    )
    
    python -m streamlit run app.py %*
    if errorlevel 1 (
        echo.
        echo [ERROR] Failed to start application
        pause
        exit /b 1
    )
)

pause

