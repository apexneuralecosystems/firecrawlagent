#!/usr/bin/env python3
"""
Main entry point for FireCrawl Agent RAG Application.
This script provides a command-line interface to run the application.
"""

import sys
import os
import argparse
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

def check_environment():
    """Check if required environment variables are set."""
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = {
        "FIRECRAWL_API_KEY": os.getenv("FIRECRAWL_API_KEY"),
        "OPENROUTER_API_KEY": os.getenv("OPENROUTER_API_KEY"),
    }
    
    missing = [key for key, value in required_vars.items() if not value]
    
    if missing:
        print("❌ Missing required environment variables:")
        for var in missing:
            print(f"   - {var}")
        print("\n💡 Please create a .env file in the project root with:")
        for var in missing:
            print(f"   {var}=your_{var.lower()}_here")
        print("\nOr set them as environment variables.")
        return False
    
    return True

def check_dependencies():
    """Check if required Python packages are installed."""
    # Map package names (as they appear in requirements.txt) to their import names
    required_packages = {
        "streamlit": "streamlit",
        "llama-index": "llama_index",
        "chromadb": "chromadb",
        # "fastembed": "fastembed",  # Optional: disabled due to version incompatibility
        "litellm": "litellm",
        "python-dotenv": "dotenv",  # python-dotenv is imported as 'dotenv'
    }
    
    missing = []
    for package_name, import_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing.append(package_name)
    
    if missing:
        print("❌ Missing required Python packages:")
        for pkg in missing:
            print(f"   - {pkg}")
        print("\n💡 Please install dependencies using:")
        print("   pip install -r requirements.txt")
        print("   or")
        print("   uv sync")
        return False
    
    return True

def run_streamlit_app(port=8501, host="localhost"):
    """Run the Streamlit application."""
    import subprocess
    import sys
    
    print(f"🚀 Starting FireCrawl Agent Application...")
    print(f"📡 Server will be available at: http://{host}:{port}")
    print("\n" + "="*60)
    print("Press Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    try:
        # Run streamlit
        cmd = [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "app.py",
            "--server.port", str(port),
            "--server.address", host,
            "--server.headless", "true",
        ]
        
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down gracefully...")
        sys.exit(0)
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error running Streamlit: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("\n❌ Streamlit not found. Please install it using:")
        print("   pip install streamlit")
        sys.exit(1)

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="FireCrawl Agent RAG Application",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Run with default settings
  python main.py --port 8080        # Run on custom port
  python main.py --check-only       # Only check setup, don't run
  python main.py --skip-checks      # Skip environment checks (not recommended)
        """
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=8501,
        help="Port to run the Streamlit app on (default: 8501)"
    )
    
    parser.add_argument(
        "--host",
        type=str,
        default="localhost",
        help="Host to bind the server to (default: localhost)"
    )
    
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Only perform setup checks, don't run the app"
    )
    
    parser.add_argument(
        "--skip-checks",
        action="store_true",
        help="Skip environment and dependency checks (not recommended)"
    )
    
    args = parser.parse_args()
    
    # Print banner
    print("="*60)
    print("🤖 FireCrawl Agent RAG Application")
    print("="*60)
    print()
    
    # Perform checks unless skipped
    if not args.skip_checks:
        print("🔍 Checking setup...")
        print()
        
        # Check dependencies
        print("📦 Checking dependencies...")
        if not check_dependencies():
            sys.exit(1)
        print("✅ All dependencies are installed")
        print()
        
        # Check environment
        print("🔑 Checking environment variables...")
        if not check_environment():
            sys.exit(1)
        print("✅ All environment variables are set")
        print()
    
    # If check-only mode, exit here
    if args.check_only:
        print("✅ All checks passed! Ready to run.")
        sys.exit(0)
    
    # Run the application
    run_streamlit_app(port=args.port, host=args.host)

if __name__ == "__main__":
    main()
