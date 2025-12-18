#!/bin/bash
# Unix/Linux/Mac launcher script for FireCrawl Agent RAG Application

echo "============================================================"
echo "  FireCrawl Agent RAG Application"
echo "============================================================"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "[ERROR] Python is not installed or not in PATH"
        echo "Please install Python 3.11 or later and try again."
        exit 1
    else
        PYTHON_CMD=python
    fi
else
    PYTHON_CMD=python3
fi

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1)
echo "[INFO] Python found: $PYTHON_VERSION"
echo ""

# Check if main.py exists (preferred method)
if [ -f "main.py" ]; then
    echo "[INFO] Starting application using main.py..."
    echo ""
    
    $PYTHON_CMD main.py "$@"
    
    if [ $? -ne 0 ]; then
        echo ""
        echo "[ERROR] Failed to start application"
        exit 1
    fi
else
    # Fallback to direct streamlit command
    echo "[INFO] Starting application using streamlit directly..."
    echo ""
    
    # Check if streamlit is available
    if ! $PYTHON_CMD -m streamlit --version &> /dev/null; then
        echo "[ERROR] Streamlit is not installed"
        echo "Please install dependencies: pip install -r requirements.txt"
        exit 1
    fi
    
    $PYTHON_CMD -m streamlit run app.py "$@"
    
    if [ $? -ne 0 ]; then
        echo ""
        echo "[ERROR] Failed to start application"
        exit 1
    fi
fi





