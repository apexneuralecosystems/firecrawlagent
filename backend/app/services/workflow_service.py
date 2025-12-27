"""
Workflow Service - Handles document processing and query execution
Extracted from app.py without Streamlit dependencies
"""
import os
import sys
import tempfile
import asyncio
from contextlib import redirect_stdout
import io
from typing import Optional, Tuple

# Add project root to path to import agentic_workflow and other modules
# This file is at: backend/app/services/workflow_service.py
# Project root is: backend/../ (firecrawlagent/)
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
project_root = os.path.dirname(backend_dir)

# IMPORTANT: Add project root but ensure backend/app takes precedence over root app.py
# We add project root at position 1 (not 0) to avoid importing root app.py
if project_root not in sys.path:
    # Check if backend_dir is already in path (should be from main.py)
    if backend_dir in sys.path:
        backend_idx = sys.path.index(backend_dir)
        sys.path.insert(backend_idx + 1, project_root)
    else:
        # If backend_dir not in path, add it first, then project root
        sys.path.insert(0, backend_dir)
        sys.path.insert(1, project_root)

# Import necessary modules
from llama_index.core import Settings, StorageContext, SimpleDirectoryReader
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.litellm import LiteLLM
from agentic_workflow import AgenticRAGWorkflow
import chromadb
import pydantic_config  # noqa: F401
from app.config import get_settings


class WorkflowService:
    """Service for managing RAG workflows."""
    
    @staticmethod
    def _safe_set_embed_model(embed_model):
        """
        Safely set the embed_model on Settings using direct assignment.
        
        We NEVER use Settings.embed_model = embed_model because it triggers
        langchain_community imports that have Pydantic v1 BaseMessage validation errors.
        """
        Settings._embed_model = embed_model
    
    @staticmethod
    def _create_embedding_model_safe(model_name: str = "text-embedding-3-small"):
        """
        Create OpenAI embedding model via OpenRouter API.
        
        Args:
            model_name: OpenAI embedding model name
            
        Returns:
            OpenAIEmbedding instance configured for OpenRouter
        """
        from pydantic import ValidationError
        
        try:
            embed_model = OpenAIEmbedding(
                model=model_name,
                api_key=os.getenv("OPENROUTER_API_KEY"),
                api_base="https://openrouter.ai/api/v1",
            )
            return embed_model
        except (ValidationError, TypeError) as e:
            error_msg = str(e)
            if "BaseMessage" in error_msg or "arbitrary_types_allowed" in error_msg:
                try:
                    from pydantic import ConfigDict
                    OpenAIEmbedding.model_config = ConfigDict(arbitrary_types_allowed=True)
                    if hasattr(OpenAIEmbedding, '__pydantic_config__'):
                        OpenAIEmbedding.__pydantic_config__ = ConfigDict(arbitrary_types_allowed=True)
                    
                    return OpenAIEmbedding(
                        model=model_name,
                        api_key=os.getenv("OPENROUTER_API_KEY"),
                        api_base="https://openrouter.ai/api/v1",
                    )
                except Exception as e2:
                    raise e from e2
            else:
                raise
    
    @staticmethod
    def _load_embedding_model(model_name: str = "text-embedding-3-small"):
        """
        Load and cache the OpenAI embedding model via OpenRouter API.
        """
        try:
            embed_model = WorkflowService._create_embedding_model_safe(model_name)
            WorkflowService._safe_set_embed_model(embed_model)
            return embed_model
        except Exception as e:
            # Try fallback model
            try:
                embed_model = WorkflowService._create_embedding_model_safe("text-embedding-ada-002")
                WorkflowService._safe_set_embed_model(embed_model)
                return embed_model
            except Exception as e2:
                raise RuntimeError(
                    f"Failed to load embedding model. Original: {e}, Fallback: {e2}"
                ) from e2
    
    @staticmethod
    def _load_llm():
        """Load and cache the LLM model."""
        model = os.getenv("LLM_MODEL", "openrouter/google/gemini-2.0-flash-exp:free")
        
        llm = LiteLLM(
            model=model,
            api_base="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY")
        )
        
        display_name = model.replace("openrouter/", "") if model.startswith("openrouter/") else model
        print(f"✅ LLM loaded: {display_name}")
        return llm
    
    @staticmethod
    def _create_custom_index(vector_store, storage_context, embed_model, nodes):
        """Create custom index wrapper to avoid Pydantic issues."""
        
        class CustomVectorIndex:
            """Custom index that wraps vector store without triggering problematic imports."""
            def __init__(self, vector_store, storage_context, embed_model, nodes):
                self._vector_store = vector_store
                self._storage_context = storage_context
                self._embed_model = embed_model
                self._nodes = nodes
                self.vector_store = vector_store
                self.storage_context = storage_context
                self.embed_model = embed_model
                self.docstore = storage_context.docstore if storage_context else None
                self.index_struct = None
                self._index_struct = None
            
            def as_retriever(self, similarity_top_k=5, **kwargs):
                """Create a simple retriever."""
                from llama_index.core.retrievers import VectorIndexRetriever
                return VectorIndexRetriever(
                    index=self,
                    similarity_top_k=similarity_top_k,
                    vector_store=self._vector_store,
                    embed_model=self._embed_model,
                )
            
            def as_query_engine(self, llm=None, **kwargs):
                """Create a query engine."""
                from llama_index.core.query_engine import RetrieverQueryEngine
                retriever = self.as_retriever(**kwargs)
                return RetrieverQueryEngine(retriever=retriever, llm=llm or Settings.llm)
            
            @property
            def ref_doc_info(self):
                """Return reference document info."""
                return {}
            
            def __getattr__(self, name):
                """Fallback for any missing attributes."""
                if name.startswith('_'):
                    raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
                print(f"Warning: Accessing missing attribute '{name}' on CustomVectorIndex")
                return None
        
        return CustomVectorIndex(vector_store, storage_context, embed_model, nodes)
    
    @staticmethod
    def _collection_name_for_session(session_id: str) -> str:
        # Chroma collection names should be stable and avoid special characters where possible.
        safe = session_id.replace("-", "")
        return f"session_{safe}"

    @staticmethod
    def delete_vector_collection_for_session(session_id: str) -> None:
        """
        Best-effort deletion of the per-session Chroma collection.
        This keeps session deletion aligned with privacy expectations.
        """
        try:
            settings = get_settings()
            chroma_client = chromadb.PersistentClient(path=settings.chroma_db_path)
            chroma_client.delete_collection(name=WorkflowService._collection_name_for_session(session_id))
        except Exception as e:
            # Best-effort cleanup; don't fail session deletion due to cleanup errors.
            print(f"Warning: Failed to delete Chroma collection for session {session_id}: {e}")

    async def process_document(self, file_path: str, session_id: str):
        """
        Process uploaded document and return workflow.
        
        Args:
            file_path: Path to directory containing the document
            
        Returns:
            AgenticRAGWorkflow instance
        """
        # Ensure pydantic_config is imported
        import pydantic_config  # noqa: F401
        
        print("📚 Loading documents...")
        try:
            documents = SimpleDirectoryReader(file_path).load_data()
            print(f"DEBUG: Loaded {len(documents)} documents")
        except Exception as e:
            raise ValueError(f"Failed to load documents: {e}")
        
        settings = get_settings()
        print("🗄️ Setting up vector store...")
        # Set up ChromaDB client
        chroma_client = chromadb.PersistentClient(path=settings.chroma_db_path)
        collection_name = self._collection_name_for_session(session_id)
        chroma_collection = chroma_client.get_or_create_collection(collection_name)
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        print("DEBUG: Chroma vector store created")
        
        print("⚙️ Initializing embedding model...")
        try:
            embed_model = self._load_embedding_model("text-embedding-3-small")
            print("DEBUG: Embedding model loaded and cached")
        except Exception as e:
            error_msg = str(e).lower()
            if "basemessage" in error_msg or "arbitrary_types_allowed" in error_msg:
                print("Primary model failed, trying fallback model...")
                embed_model = self._load_embedding_model("text-embedding-ada-002")
                print("DEBUG: Fallback embedding model loaded")
            else:
                raise
        
        print("🤖 Loading language model...")
        llm = self._load_llm()
        print("DEBUG: LLM loaded")
        
        Settings.llm = llm
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        print("DEBUG: Storage context created")
        
        print("🔍 Creating document index...")
        try:
            self._safe_set_embed_model(embed_model)
            
            # Parse documents into nodes
            node_parser = SimpleNodeParser.from_defaults()
            nodes = node_parser.get_nodes_from_documents(documents)
            
            # Embed nodes
            print(f"DEBUG: Embedding {len(nodes)} nodes")
            for i, node in enumerate(nodes):
                if hasattr(node, 'get_content'):
                    text = node.get_content()
                else:
                    text = getattr(node, 'text', '')
                
                if text:
                    try:
                        embedding = embed_model.get_text_embedding(text)
                        node.embedding = embedding
                    except Exception as e:
                        print(f"Warning: Failed to embed node: {e}")
                        node.embedding = None
            
            print(f"DEBUG: All {len(nodes)} nodes embedded")
            
            # Store nodes in vector store
            print("💾 Storing vectors in database...")
            vector_store.add(nodes)
            print(f"DEBUG: Stored {len(nodes)} nodes in vector store")
            
            # Create custom index
            print("🔗 Creating index wrapper...")
            index = self._create_custom_index(
                vector_store, storage_context, embed_model, nodes
            )
            
            print("DEBUG: Custom index wrapper created - SUCCESS!")
            
        except Exception as index_error:
            import traceback
            error_trace = traceback.format_exc()
            print(f"Index creation error:\n{error_trace}")
            raise RuntimeError(f"Failed to create index: {index_error}") from index_error
        
        # Check if FIRECRAWL_API_KEY is available
        if "FIRECRAWL_API_KEY" not in os.environ:
            raise ValueError("FireCrawl API key not found in environment variables.")
        
        # Create workflow
        try:
            workflow = AgenticRAGWorkflow(
                index=index,
                firecrawl_api_key=os.environ["FIRECRAWL_API_KEY"],
                verbose=True,
                timeout=249,
                llm=llm
            )
            print("DEBUG: Workflow created successfully")
        except Exception as workflow_error:
            error_str = str(workflow_error)
            if "BaseMessage" in error_str or "arbitrary_types_allowed" in error_str:
                print("⚠️ BaseMessage validation error detected. Attempting to fix...")
                try:
                    from pydantic import ConfigDict
                    if not hasattr(AgenticRAGWorkflow, 'model_config') or \
                       (hasattr(AgenticRAGWorkflow.model_config, 'get') and 
                        not AgenticRAGWorkflow.model_config.get('arbitrary_types_allowed')):
                        AgenticRAGWorkflow.model_config = ConfigDict(arbitrary_types_allowed=True)
                    
                    from llama_index.core.workflow import Workflow
                    Workflow.model_config = ConfigDict(arbitrary_types_allowed=True)
                    
                    import importlib
                    import pydantic_config
                    importlib.reload(pydantic_config)
                    
                    workflow = AgenticRAGWorkflow(
                        index=index,
                        firecrawl_api_key=os.environ["FIRECRAWL_API_KEY"],
                        verbose=True,
                        timeout=249,
                        llm=llm
                    )
                    print("✅ Fixed BaseMessage validation error!")
                    print("DEBUG: Workflow created successfully after retry")
                except Exception as fix_error:
                    raise workflow_error from fix_error
            else:
                raise
        
        print("✅ Document processing complete!")
        return workflow, collection_name
    
    async def run_query(self, workflow, query: str) -> Tuple[any, str]:
        """
        Run query through workflow.
        
        Args:
            workflow: AgenticRAGWorkflow instance
            query: User query string
            
        Returns:
            Tuple of (result, logs)
        """
        f = io.StringIO()
        with redirect_stdout(f):
            result = await asyncio.wait_for(
                workflow.run(query_str=query),
                timeout=300  # 5 minutes timeout
            )
        
        logs = f.getvalue()
        return result, logs

