"""
ChromaDB + Pydantic v1 Compatibility for Python 3.14.

Python 3.14 introduces changes to typing (deferred evaluation) that break Pydantic v1.10.x's
type inference logic, causing `ConfigError: unable to infer type` even for annotated fields.
Since ChromaDB relies on Pydantic v1 and we are on Python 3.14, we must patch Pydantic v1
to handle these failures gracefully by falling back to `Any`.
"""
import sys
from typing import Any

def ensure_chromadb_pydantic_compat():
    """
    Monkey-patch pydantic.v1.fields.ModelField._type_analysis to handle
    Python 3.14 compatibility issues.
    """
    try:
        # Try importing pydantic.v1 (used by ChromaDB)
        try:
            from pydantic.v1 import fields, errors
        except ImportError:
            # If pydantic.v1 is not available, nothing to patch
            return

        # Check if we already patched it
        if getattr(fields.ModelField, '_patch_applied', False):
            return

        # Save original method
        _orig_type_analysis = fields.ModelField._type_analysis
        print(f"DEBUG: Patching ModelField._type_analysis. Original: {_orig_type_analysis}")

        def _patched_type_analysis(self):
            try:
                return _orig_type_analysis(self)
            except errors.ConfigError as e:
                print(f"DEBUG: Caught ConfigError in _type_analysis: {e}")
                # Python 3.14 + Pydantic v1 compat shim
                # If type inference fails, fallback to Any
                # Broaden check for debugging
                self.type_ = Any
                self.outer_type_ = Any
                self.sub_fields = None
                self.key_field = None
                self.validators = [] 
                self.pre_validators = []
                self.post_validators = []
                return
                
        # Apply patch
        fields.ModelField._type_analysis = _patched_type_analysis
        fields.ModelField._patch_applied = True
        print("DEBUG: ModelField._type_analysis patch APPLIED.")

        
    except (ImportError, AttributeError):
        pass
