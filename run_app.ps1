# PowerShell script to run the Streamlit app
# FireCrawl Agent RAG Application Launcher

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  FireCrawl Agent RAG Application" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[INFO] Python found: $pythonVersion" -ForegroundColor Green
    Write-Host ""
} catch {
    Write-Host "[ERROR] Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.11 or later and try again." -ForegroundColor Yellow
    exit 1
}

# Check if main.py exists (preferred method)
if (Test-Path "main.py") {
    Write-Host "[INFO] Starting application using main.py..." -ForegroundColor Green
    Write-Host ""
    
    $args_string = $args -join " "
    python main.py $args_string
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "[ERROR] Failed to start application" -ForegroundColor Red
        exit 1
    }
} else {
    # Fallback to direct streamlit command
    Write-Host "[INFO] Starting application using streamlit directly..." -ForegroundColor Green
    Write-Host ""
    
    # Check if streamlit is available
    try {
        $streamlitVersion = python -m streamlit --version 2>&1
        Write-Host "[INFO] Streamlit found" -ForegroundColor Green
    } catch {
        Write-Host "[ERROR] Streamlit is not installed" -ForegroundColor Red
        Write-Host "Please install dependencies: pip install -r requirements.txt" -ForegroundColor Yellow
        exit 1
    }
    
    $args_string = $args -join " "
    python -m streamlit run app.py $args_string
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "[ERROR] Failed to start application" -ForegroundColor Red
        exit 1
    }
}
