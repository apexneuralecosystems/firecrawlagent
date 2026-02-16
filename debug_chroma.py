"""Test if pydantic.v1 BaseSettings works with Optional annotations."""
import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

from typing import Optional
from pydantic.v1 import BaseSettings

class TestSettings(BaseSettings):
    x: Optional[str] = None

try:
    t = TestSettings()
    print(f"OK: {t}")
except Exception as e:
    print(f"FAIL: {type(e).__name__}: {e}")

# Now try importing chromadb directly
import traceback
try:
    import chromadb
    print(f"ChromaDB OK: {chromadb.__version__}")
except Exception as e:
    print(f"ChromaDB FAIL: {type(e).__name__}: {e}")
    # Get the specific field name from the traceback
    traceback.print_exc()
