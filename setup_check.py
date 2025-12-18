#!/usr/bin/env python3
"""
Setup verification script for FireCrawl Agent RAG Application.
Checks all prerequisites and provides helpful error messages.
"""

import sys
import os
from pathlib import Path

def print_header(text):
    """Print a formatted header."""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def check_python_version():
    """Check if Python version is compatible."""
    print_header("Checking Python Version")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print(f"❌ Python 3.11+ required. Found: {version.major}.{version.minor}.{version.micro}")
        print("   Please upgrade Python to version 3.11 or later.")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} (Compatible)")
    return True

def check_dependencies():
    """Check if required packages are installed."""
    print_header("Checking Dependencies")
    
    # Map package names to their import names and descriptions
    required = {
        ("streamlit", "streamlit"): "Streamlit web framework",
        ("llama-index", "llama_index"): "LlamaIndex RAG framework",
        ("llama_index.core", "llama_index.core"): "LlamaIndex core",
        ("chromadb", "chromadb"): "ChromaDB vector database",
        ("fastembed", "fastembed"): "FastEmbed embeddings",
        ("litellm", "litellm"): "LiteLLM for LLM access",
        ("python-dotenv", "dotenv"): "Environment variable management",  # python-dotenv imports as 'dotenv'
        ("requests", "requests"): "HTTP requests",
    }
    
    missing = []
    installed = []
    
    for (package_name, import_name), description in required.items():
        try:
            __import__(import_name)
            installed.append(package_name)
            print(f"✅ {package_name:25s} - {description}")
        except ImportError:
            missing.append(package_name)
            print(f"❌ {package_name:25s} - {description} (NOT INSTALLED)")
    
    if missing:
        print(f"\n⚠️  {len(missing)} package(s) missing:")
        for pkg in missing:
            print(f"   - {pkg}")
        print("\n💡 Install missing packages using:")
        print("   pip install -r requirements.txt")
        print("   or")
        print("   uv sync")
        return False
    
    print(f"\n✅ All {len(installed)} required packages are installed")
    return True

def check_environment_variables():
    """Check if required environment variables are set."""
    print_header("Checking Environment Variables")
    
    # Load .env file if it exists
    from dotenv import load_dotenv
    env_file = Path(".env")
    
    if env_file.exists():
        print("📄 Found .env file")
        load_dotenv()
    else:
        print("⚠️  No .env file found (will check environment variables only)")
    
    required = {
        "FIRECRAWL_API_KEY": "FireCrawl API key for web search",
        "OPENROUTER_API_KEY": "OpenRouter API key for LLM access",
    }
    
    missing = []
    present = []
    
    for var, description in required.items():
        value = os.getenv(var)
        if value:
            # Mask the key (show first 8 chars)
            masked = value[:8] + "..." if len(value) > 8 else value
            present.append(var)
            print(f"✅ {var:25s} - {description} (Set: {masked})")
        else:
            missing.append(var)
            print(f"❌ {var:25s} - {description} (NOT SET)")
    
    if missing:
        print(f"\n⚠️  {len(missing)} environment variable(s) missing:")
        for var in missing:
            print(f"   - {var}")
        print("\n💡 Create a .env file in the project root with:")
        print("   FIRECRAWL_API_KEY=your_firecrawl_api_key_here")
        print("   OPENROUTER_API_KEY=your_openrouter_api_key_here")
        print("\n   Or set them as environment variables.")
        return False
    
    print(f"\n✅ All {len(present)} environment variables are set")
    return True

def check_directories():
    """Check if required directories exist or can be created."""
    print_header("Checking Directories")
    
    required_dirs = [
        "chroma_db",
        "hf_cache",
    ]
    
    all_ok = True
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            if dir_path.is_dir():
                print(f"✅ {dir_name:25s} - Directory exists")
            else:
                print(f"❌ {dir_name:25s} - Exists but is not a directory")
                all_ok = False
        else:
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
                print(f"✅ {dir_name:25s} - Created")
            except Exception as e:
                print(f"❌ {dir_name:25s} - Cannot create: {e}")
                all_ok = False
    
    return all_ok

def check_optional_dependencies():
    """Check optional dependencies that enhance functionality."""
    print_header("Checking Optional Dependencies")
    
    optional = {
        "qdrant_client": "Qdrant vector store support",
        "llama_index.vector_stores.milvus": "Milvus vector store support",
        "playwright": "Enhanced web scraping capabilities",
    }
    
    for package, description in optional.items():
        try:
            import_name = package.replace(".", "_")
            __import__(package.replace(".", "_"))
            print(f"✅ {package:30s} - {description}")
        except ImportError:
            print(f"⚪ {package:30s} - {description} (Optional, not installed)")

def main():
    """Run all setup checks."""
    print("="*60)
    print("🔍 FireCrawl Agent - Setup Verification")
    print("="*60)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Environment Variables", check_environment_variables),
        ("Directories", check_directories),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Error during {name} check: {e}")
            results.append((name, False))
    
    # Optional checks (don't affect pass/fail)
    try:
        check_optional_dependencies()
    except Exception as e:
        print(f"\n⚠️  Error during optional dependency check: {e}")
    
    # Summary
    print_header("Summary")
    
    all_passed = all(result for _, result in results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:10s} - {name}")
    
    if all_passed:
        print("\n🎉 All critical checks passed! You're ready to run the application.")
        print("\n💡 To start the application, run:")
        print("   python main.py")
        print("   or")
        print("   streamlit run app.py")
        return 0
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above before running.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
