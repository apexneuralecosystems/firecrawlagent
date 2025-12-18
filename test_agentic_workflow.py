"""
Test suite for Agentic RAG Workflow with mock documents.
"""
import os
import sys
import tempfile
import asyncio
from pathlib import Path
import pytest

# Set environment variables for testing
os.environ["PYDANTIC_ALLOW_ARBITRARY_TYPES"] = "true"
os.environ.setdefault("FIRECRAWL_API_KEY", "test_key")
os.environ.setdefault("OPENROUTER_API_KEY", "test_key")

# IMPORTANT: Import pydantic_config FIRST to patch base classes
import pydantic_config  # noqa: F401

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings, StorageContext
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.litellm import LiteLLM
import chromadb

# Import the agentic workflow
from agentic_workflow import (
    AgenticRAGWorkflow,
    RetrievalAgent,
    RelevanceAgent,
    WebSearchAgent,
    QueryAgent,
    OrchestratorAgent,
    Agent
)


def create_mock_documents():
    """Create mock PDF-like documents for testing."""
    mock_docs = [
        {
            "filename": "test_doc1.txt",
            "content": """
            Artificial Intelligence and Machine Learning
            
            Artificial Intelligence (AI) is a branch of computer science that aims to create 
            intelligent machines capable of performing tasks that typically require human intelligence.
            Machine Learning is a subset of AI that enables systems to learn and improve from 
            experience without being explicitly programmed.
            
            Key concepts include:
            - Neural networks
            - Deep learning
            - Natural language processing
            - Computer vision
            
            Applications of AI include autonomous vehicles, healthcare diagnostics, and 
            recommendation systems.
            """
        },
        {
            "filename": "test_doc2.txt",
            "content": """
            Python Programming Language
            
            Python is a high-level, interpreted programming language known for its simplicity 
            and readability. It was created by Guido van Rossum and first released in 1991.
            
            Python features:
            - Dynamic typing
            - Automatic memory management
            - Extensive standard library
            - Large ecosystem of third-party packages
            
            Python is widely used in:
            - Web development (Django, Flask)
            - Data science (Pandas, NumPy)
            - Machine learning (TensorFlow, PyTorch)
            - Automation and scripting
            """
        },
        {
            "filename": "test_doc3.txt",
            "content": """
            Vector Databases and Embeddings
            
            Vector databases are specialized databases designed to store and query high-dimensional 
            vectors efficiently. They are essential for similarity search and retrieval-augmented 
            generation (RAG) systems.
            
            Popular vector databases include:
            - ChromaDB
            - Qdrant
            - Milvus
            - Pinecone
            
            Embeddings are numerical representations of text, images, or other data that capture 
            semantic meaning. They enable semantic search and similarity matching.
            
            Use cases:
            - Document search
            - Recommendation systems
            - Anomaly detection
            - Image similarity search
            """
        }
    ]
    return mock_docs


def setup_test_environment():
    """Set up test environment with mock documents."""
    # Create temporary directory for test documents
    temp_dir = tempfile.mkdtemp()
    
    # Create mock documents
    mock_docs = create_mock_documents()
    for doc in mock_docs:
        file_path = Path(temp_dir) / doc["filename"]
        file_path.write_text(doc["content"], encoding="utf-8")
    
    return temp_dir, mock_docs


def setup_vector_store(temp_dir):
    """Set up vector store with test documents."""
    # Load documents
    documents = SimpleDirectoryReader(temp_dir).load_data()
    
    # Set up embedding model
    embed_model = FastEmbedEmbedding(
        model_name="BAAI/bge-small-en-v1.5",  # Smaller model for faster testing
        cache_dir="./hf_cache"
    )
    Settings.embed_model = embed_model
    
    # Set up ChromaDB
    chroma_client = chromadb.PersistentClient(path="./test_chroma_db")
    chroma_collection = chroma_client.get_or_create_collection("test_collection")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    
    # Create storage context
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    
    # Create index
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
    )
    
    return index, documents


def test_mock_documents_creation():
    """Test that mock documents are created correctly."""
    print("\n[TEST 1] Mock Documents Creation")
    temp_dir, mock_docs = setup_test_environment()
    
    assert len(mock_docs) == 3, "Should have 3 mock documents"
    assert Path(temp_dir).exists(), "Temp directory should exist"
    
    for doc in mock_docs:
        file_path = Path(temp_dir) / doc["filename"]
        assert file_path.exists(), f"File {doc['filename']} should exist"
        assert len(file_path.read_text()) > 0, f"File {doc['filename']} should have content"
    
    print("[OK] Mock documents created successfully")
    return temp_dir, mock_docs


def test_vector_store_setup():
    """Test vector store setup with mock documents."""
    print("\n[TEST 2] Vector Store Setup")
    temp_dir, _ = setup_test_environment()
    index, documents = setup_vector_store(temp_dir)
    
    assert index is not None, "Index should be created"
    assert len(documents) == 3, "Should have 3 documents"
    
    # Test retrieval
    retriever = index.as_retriever(similarity_top_k=2)
    results = retriever.retrieve("What is artificial intelligence?")
    
    assert len(results) > 0, "Should retrieve at least one result"
    print(f"[OK] Vector store setup successful. Retrieved {len(results)} results")
    
    return index


def test_retrieval_agent():
    """Test RetrievalAgent."""
    print("\n[TEST 3] RetrievalAgent")
    temp_dir, _ = setup_test_environment()
    index, _ = setup_vector_store(temp_dir)
    
    # Create mock LLM
    llm = LiteLLM(model="openrouter/google/gemini-flash-1.5", api_key=os.getenv("OPENROUTER_API_KEY"))
    
    # Create retrieval agent
    retriever = index.as_retriever()
    agent = RetrievalAgent("TestRetrievalAgent", llm, retriever)
    
    # Test agent execution
    async def run_test():
        result = await agent.execute("What is Python?")
        assert result["agent"] == "TestRetrievalAgent"
        assert result["task"] == "retrieval"
        assert result["status"] == "success"
        assert len(result["result"]) > 0, "Should retrieve documents"
        print(f"[OK] RetrievalAgent test passed. Retrieved {len(result['result'])} documents")
        return result
    
    result = asyncio.run(run_test())
    return result


def test_relevance_agent():
    """Test RelevanceAgent."""
    print("\n[TEST 4] RelevanceAgent")
    temp_dir, _ = setup_test_environment()
    index, _ = setup_vector_store(temp_dir)
    
    # Get some nodes
    retriever = index.as_retriever()
    nodes = retriever.retrieve("Python programming")
    
    # Create mock LLM
    llm = LiteLLM(model="openrouter/google/gemini-flash-1.5", api_key=os.getenv("OPENROUTER_API_KEY"))
    
    # Create relevance agent
    agent = RelevanceAgent("TestRelevanceAgent", llm)
    
    # Test agent execution
    async def run_test():
        context = {
            "nodes": nodes,
            "query": "What is Python programming language?"
        }
        result = await agent.execute("Evaluate relevance", context)
        assert result["agent"] == "TestRelevanceAgent"
        assert result["task"] == "relevance_evaluation"
        assert result["status"] == "success"
        print(f"[OK] RelevanceAgent test passed. Evaluated {len(nodes)} documents")
        return result
    
    result = asyncio.run(run_test())
    return result


def test_web_search_agent():
    """Test WebSearchAgent (mocked)."""
    print("\n[TEST 5] WebSearchAgent")
    
    # Create mock LLM
    llm = LiteLLM(model="openrouter/google/gemini-flash-1.5", api_key=os.getenv("OPENROUTER_API_KEY"))
    
    # Create web search agent
    agent = WebSearchAgent("TestWebSearchAgent", llm, "test_api_key")
    
    # Test agent structure
    assert agent.name == "TestWebSearchAgent"
    assert agent.firecrawl_api_key == "test_api_key"
    print("[OK] WebSearchAgent structure test passed")
    
    # Note: Actual web search test would require real API key
    return agent


def test_query_agent():
    """Test QueryAgent."""
    print("\n[TEST 6] QueryAgent")
    
    # Create mock LLM
    llm = LiteLLM(model="openrouter/google/gemini-flash-1.5", api_key=os.getenv("OPENROUTER_API_KEY"))
    
    # Create query agent
    agent = QueryAgent("TestQueryAgent", llm)
    
    # Test agent execution
    async def run_test():
        context = {
            "relevant_text": "Python is a programming language.",
            "search_text": "",
            "query": "What is Python?"
        }
        result = await agent.execute("Generate answer", context)
        assert result["agent"] == "TestQueryAgent"
        assert result["task"] == "answer_generation"
        assert result["status"] == "success"
        assert len(result["result"]) > 0, "Should generate an answer"
        print(f"[OK] QueryAgent test passed. Generated answer: {result['result'][:50]}...")
        return result
    
    result = asyncio.run(run_test())
    return result


def test_agentic_workflow():
    """Test the complete AgenticRAGWorkflow."""
    print("\n[TEST 7] Complete AgenticRAGWorkflow")
    temp_dir, _ = setup_test_environment()
    index, _ = setup_vector_store(temp_dir)
    
    # Create workflow
    workflow = AgenticRAGWorkflow(
        index=index,
        firecrawl_api_key="test_key",
        verbose=False
    )
    
    assert workflow is not None, "Workflow should be created"
    assert workflow.orchestrator is not None, "Orchestrator should be created"
    assert workflow.retrieval_agent is not None, "RetrievalAgent should be created"
    assert workflow.relevance_agent is not None, "RelevanceAgent should be created"
    assert workflow.web_search_agent is not None, "WebSearchAgent should be created"
    assert workflow.query_agent is not None, "QueryAgent should be created"
    
    print("[OK] AgenticRAGWorkflow structure test passed")
    
    # Test workflow execution
    async def run_test():
        result = await workflow.run(query_str="What is Python?")
        assert result is not None, "Workflow should return a result"
        print(f"[OK] AgenticRAGWorkflow execution test passed")
        return result
    
    result = asyncio.run(run_test())
    return result


def test_document_upload_simulation():
    """Simulate document upload and processing."""
    print("\n[TEST 8] Document Upload Simulation")
    
    # Simulate upload
    temp_dir, mock_docs = setup_test_environment()
    
    # Simulate processing
    documents = SimpleDirectoryReader(temp_dir).load_data()
    assert len(documents) == len(mock_docs), "Should process all uploaded documents"
    
    # Simulate indexing
    index, _ = setup_vector_store(temp_dir)
    assert index is not None, "Index should be created"
    
    # Simulate query
    retriever = index.as_retriever()
    results = retriever.retrieve("artificial intelligence")
    assert len(results) > 0, "Should retrieve relevant documents"
    
    print(f"[OK] Document upload simulation passed. Processed {len(documents)} documents")
    return index


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("[TEST] Running Agentic RAG Workflow Tests")
    print("=" * 60)
    
    results = {
        "passed": 0,
        "failed": 0,
        "errors": []
    }
    
    tests = [
        ("Mock Documents Creation", test_mock_documents_creation),
        ("Vector Store Setup", test_vector_store_setup),
        ("RetrievalAgent", test_retrieval_agent),
        ("RelevanceAgent", test_relevance_agent),
        ("WebSearchAgent", test_web_search_agent),
        ("QueryAgent", test_query_agent),
        ("Complete Workflow", test_agentic_workflow),
        ("Document Upload Simulation", test_document_upload_simulation),
    ]
    
    for test_name, test_func in tests:
        try:
            print(f"\n{'='*60}")
            print(f"Running: {test_name}")
            print(f"{'='*60}")
            test_func()
            results["passed"] += 1
            print(f"[PASS] {test_name} PASSED")
        except Exception as e:
            results["failed"] += 1
            results["errors"].append((test_name, str(e)))
            print(f"[FAIL] {test_name} FAILED: {e}")
            import traceback
            traceback.print_exc()
    
    # Print summary
    print("\n" + "=" * 60)
    print("[SUMMARY] Test Summary")
    print("=" * 60)
    print(f"[OK] Passed: {results['passed']}")
    print(f"[FAIL] Failed: {results['failed']}")
    total = results['passed'] + results['failed']
    if total > 0:
        print(f"[RATE] Success Rate: {results['passed']/total*100:.1f}%")
    
    if results["errors"]:
        print("\n[ERRORS] Errors:")
        for test_name, error in results["errors"]:
            print(f"  - {test_name}: {error}")
    
    print("=" * 60)
    
    return results


if __name__ == "__main__":
    # Run all tests
    results = run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if results["failed"] == 0 else 1)

