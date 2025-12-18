"""
Test full workflow initialization as done in app.py.
"""
import os
import sys
import tempfile
from pathlib import Path

# Set environment variables first
os.environ["PYDANTIC_ALLOW_ARBITRARY_TYPES"] = "true"
os.environ.setdefault("FIRECRAWL_API_KEY", "test_key")
os.environ.setdefault("OPENROUTER_API_KEY", "test_key")

# IMPORTANT: Import pydantic_config FIRST to patch base classes
import pydantic_config  # noqa: F401

from llama_index.core import Settings, StorageContext, VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.litellm import LiteLLM
from agentic_workflow import AgenticRAGWorkflow
import chromadb


def test_full_workflow_init():
    """Test full workflow initialization like in app.py."""
    print("\n[TEST] Full Workflow Initialization (like app.py)")
    
    temp_dir = tempfile.mkdtemp()
    
    # Create test document
    test_file = Path(temp_dir) / "test.txt"
    test_file.write_text("This is a test document about Python programming.")
    
    try:
        print("  [STEP 1] Loading documents...")
        documents = SimpleDirectoryReader(temp_dir).load_data()
        print(f"  [OK] Loaded {len(documents)} documents")
        
        print("  [STEP 2] Setting up ChromaDB...")
        chroma_client = chromadb.PersistentClient(path="./test_chroma_db_workflow")
        chroma_collection = chroma_client.get_or_create_collection("test_collection")
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        print("  [OK] Chroma vector store created")
        
        print("  [STEP 3] Initializing embedding model...")
        embed_model = FastEmbedEmbedding(
            model_name="BAAI/bge-small-en-v1.5",  # Use small model for faster test
            cache_dir="./hf_cache"
        )
        Settings.embed_model = embed_model
        print("  [OK] Embedding model initialized")
        
        print("  [STEP 4] Loading LLM...")
        llm = LiteLLM(
            model="openrouter/google/gemini-flash-1.5",
            api_key=os.getenv("OPENROUTER_API_KEY")
        )
        Settings.llm = llm
        print("  [OK] LLM loaded")
        
        print("  [STEP 5] Creating storage context...")
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        print("  [OK] Storage context created")
        
        print("  [STEP 6] Creating document index...")
        index = VectorStoreIndex.from_documents(
            documents,
            storage_context=storage_context,
        )
        print("  [OK] Index created")
        
        print("  [STEP 7] Creating AgenticRAGWorkflow...")
        workflow = AgenticRAGWorkflow(
            index=index,
            firecrawl_api_key=os.environ["FIRECRAWL_API_KEY"],
            verbose=True,
            timeout=249,
            llm=llm
        )
        print("  [OK] Workflow created successfully")
        
        print("\n[PASS] Full workflow initialization completed successfully!")
        return True, workflow
        
    except Exception as e:
        print(f"\n[FAIL] Error during workflow initialization: {e}")
        import traceback
        traceback.print_exc()
        return False, None


if __name__ == "__main__":
    print("=" * 60)
    print("[WORKFLOW INIT TEST] Testing Full Workflow Initialization")
    print("=" * 60)
    
    success, workflow = test_full_workflow_init()
    
    if success:
        print("\n" + "=" * 60)
        print("[SUCCESS] All workflow initialization steps passed!")
        print("=" * 60)
        sys.exit(0)
    else:
        print("\n" + "=" * 60)
        print("[FAILURE] Workflow initialization failed!")
        print("=" * 60)
        sys.exit(1)




