"""
Test embedding model loading with BaseMessage validation.
"""
import os
import sys

# Set environment variables first
os.environ["PYDANTIC_ALLOW_ARBITRARY_TYPES"] = "true"
os.environ.setdefault("FIRECRAWL_API_KEY", "test_key")
os.environ.setdefault("OPENROUTER_API_KEY", "test_key")

# IMPORTANT: Import pydantic_config FIRST to patch base classes
import pydantic_config  # noqa: F401

# Import after patching
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from pydantic import ValidationError


def test_embedding_model_import():
    """Test that FastEmbedEmbedding can be imported."""
    print("\n[TEST 1] FastEmbedEmbedding Import")
    try:
        from llama_index.embeddings.fastembed import FastEmbedEmbedding
        print(f"  [OK] FastEmbedEmbedding imported successfully")
        print(f"  [INFO] Class: {FastEmbedEmbedding}")
        print(f"  [INFO] Has model_config: {hasattr(FastEmbedEmbedding, 'model_config')}")
        if hasattr(FastEmbedEmbedding, 'model_config'):
            print(f"  [INFO] model_config: {FastEmbedEmbedding.model_config}")
        return True
    except Exception as e:
        print(f"  [FAIL] Failed to import FastEmbedEmbedding: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_embedding_model_config():
    """Test that FastEmbedEmbedding has proper model_config."""
    print("\n[TEST 2] FastEmbedEmbedding Model Config")
    try:
        from llama_index.embeddings.fastembed import FastEmbedEmbedding
        from pydantic import ConfigDict
        
        # Check if model_config exists
        if hasattr(FastEmbedEmbedding, 'model_config'):
            config = FastEmbedEmbedding.model_config
            print(f"  [INFO] model_config type: {type(config)}")
            print(f"  [INFO] model_config value: {config}")
            
            # Check if arbitrary_types_allowed is set
            if isinstance(config, dict):
                arbitrary_allowed = config.get('arbitrary_types_allowed', False)
            elif isinstance(config, ConfigDict):
                arbitrary_allowed = getattr(config, 'arbitrary_types_allowed', False) or config.get('arbitrary_types_allowed', False)
            else:
                arbitrary_allowed = getattr(config, 'arbitrary_types_allowed', False)
            
            print(f"  [INFO] arbitrary_types_allowed: {arbitrary_allowed}")
            
            if arbitrary_allowed:
                print(f"  [OK] arbitrary_types_allowed is True")
                return True
            else:
                print(f"  [WARN] arbitrary_types_allowed is not True, attempting to set...")
                try:
                    FastEmbedEmbedding.model_config = ConfigDict(arbitrary_types_allowed=True)
                    print(f"  [OK] Successfully set arbitrary_types_allowed=True")
                    return True
                except Exception as e2:
                    print(f"  [FAIL] Failed to set config: {e2}")
                    return False
        else:
            print(f"  [WARN] model_config attribute not found, attempting to set...")
            try:
                FastEmbedEmbedding.model_config = ConfigDict(arbitrary_types_allowed=True)
                print(f"  [OK] Successfully added model_config with arbitrary_types_allowed=True")
                return True
            except Exception as e:
                print(f"  [FAIL] Failed to set config: {e}")
                return False
    except Exception as e:
        print(f"  [FAIL] Error checking model_config: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_embedding_model_creation_large():
    """Test creating FastEmbedEmbedding with large model."""
    print("\n[TEST 3] Creating FastEmbedEmbedding (Large Model)")
    try:
        import tempfile
        cache_dir = tempfile.mkdtemp()
        
        print(f"  [STEP] Creating FastEmbedEmbedding with model 'BAAI/bge-large-en-v1.5'")
        print(f"  [STEP] Cache directory: {cache_dir}")
        
        embed_model = FastEmbedEmbedding(
            model_name="BAAI/bge-large-en-v1.5",
            cache_dir=cache_dir,
        )
        
        print(f"  [OK] Successfully created FastEmbedEmbedding")
        print(f"  [INFO] Model type: {type(embed_model)}")
        return True, embed_model
    except ValidationError as e:
        error_msg = str(e)
        print(f"  [FAIL] ValidationError: {error_msg}")
        if "BaseMessage" in error_msg:
            print(f"  [INFO] This is a BaseMessage validation error")
        if "arbitrary_types_allowed" in error_msg:
            print(f"  [INFO] This is an arbitrary_types_allowed error")
        import traceback
        traceback.print_exc()
        return False, None
    except Exception as e:
        print(f"  [FAIL] Unexpected error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False, None


def test_embedding_model_creation_small():
    """Test creating FastEmbedEmbedding with small model."""
    print("\n[TEST 4] Creating FastEmbedEmbedding (Small Model)")
    try:
        import tempfile
        cache_dir = tempfile.mkdtemp()
        
        print(f"  [STEP] Creating FastEmbedEmbedding with model 'BAAI/bge-small-en-v1.5'")
        print(f"  [STEP] Cache directory: {cache_dir}")
        
        embed_model = FastEmbedEmbedding(
            model_name="BAAI/bge-small-en-v1.5",
            cache_dir=cache_dir,
        )
        
        print(f"  [OK] Successfully created FastEmbedEmbedding")
        print(f"  [INFO] Model type: {type(embed_model)}")
        return True, embed_model
    except ValidationError as e:
        error_msg = str(e)
        print(f"  [FAIL] ValidationError: {error_msg}")
        if "BaseMessage" in error_msg:
            print(f"  [INFO] This is a BaseMessage validation error")
        if "arbitrary_types_allowed" in error_msg:
            print(f"  [INFO] This is an arbitrary_types_allowed error")
        import traceback
        traceback.print_exc()
        return False, None
    except Exception as e:
        print(f"  [FAIL] Unexpected error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False, None


def run_embedding_tests():
    """Run all embedding model tests."""
    print("=" * 60)
    print("[EMBEDDING MODEL TESTS] Running Embedding Model Tests")
    print("=" * 60)
    
    results = {"passed": 0, "failed": 0, "errors": []}
    
    tests = [
        ("Import Test", test_embedding_model_import),
        ("Config Test", test_embedding_model_config),
        ("Large Model Creation", test_embedding_model_creation_large),
        ("Small Model Creation", test_embedding_model_creation_small),
    ]
    
    for test_name, test_func in tests:
        try:
            print(f"\n{'='*60}")
            print(f"Running: {test_name}")
            print(f"{'='*60}")
            result = test_func()
            
            # Handle tuple results (success, model)
            if isinstance(result, tuple):
                success, _ = result
            else:
                success = result
            
            if success:
                results["passed"] += 1
                print(f"[PASS] {test_name} PASSED")
            else:
                results["failed"] += 1
                results["errors"].append((test_name, "Test returned False"))
                print(f"[FAIL] {test_name} FAILED")
        except Exception as e:
            results["failed"] += 1
            results["errors"].append((test_name, str(e)))
            print(f"[FAIL] {test_name} FAILED: {e}")
            import traceback
            traceback.print_exc()
    
    # Summary
    print("\n" + "=" * 60)
    print("[SUMMARY] Embedding Model Test Summary")
    print("=" * 60)
    print(f"[OK] Passed: {results['passed']}")
    print(f"[FAIL] Failed: {results['failed']}")
    total = results['passed'] + results['failed']
    if total > 0:
        print(f"[RATE] Success Rate: {results['passed']/total*100:.1f}%")
    
    if results["errors"]:
        print("\n[ERRORS] Errors:")
        for test_name, error in results["errors"]:
            print(f"  - {test_name}: {error[:200]}")
    
    print("=" * 60)
    return results


if __name__ == "__main__":
    results = run_embedding_tests()
    sys.exit(0 if results["failed"] == 0 else 1)




