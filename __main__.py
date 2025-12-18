"""
Package entry point for FireCrawl Agent RAG Application.
Allows running the package with: python -m firecrawlagnet
"""

import sys
from pathlib import Path

# Add current directory to path (not parent, since this file should be in the package root)
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Import and run main
if __name__ == "__main__":
    # Import main from the same directory
    try:
        from main import main
        main()
    except ImportError as e:
        print(f"Error: Could not import main module: {e}")
        print(f"Current directory: {current_dir}")
        sys.exit(1)

