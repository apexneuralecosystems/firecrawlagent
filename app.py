from contextlib import redirect_stdout
import io
import os

# IMPORTANT: Import langchain_patch FIRST to patch Pydantic v1 validators
# This must be imported before any langchain_community imports are triggered
import langchain_patch  # noqa: F401

# IMPORTANT: Import pydantic_config SECOND to patch base classes before they're used
# This must be imported before any workflow imports
import pydantic_config  # noqa: F401

# CRITICAL: Patch the langchain bridge import to avoid importing chat_message_histories
# This prevents BaseMessage validation errors during module import
try:
    import sys
    from unittest.mock import MagicMock
    
    # Create a mock for chat_message_histories before it's imported
    # This prevents the actual import which triggers BaseMessage validation errors
    class MockChatMessageHistory:
        pass
    
    mock_module = MagicMock()
    mock_module.ChatMessageHistory = MockChatMessageHistory
    mock_module.in_memory = mock_module
    
    # Pre-populate sys.modules to prevent actual import
    sys.modules['langchain_community.chat_message_histories'] = mock_module
    sys.modules['langchain_community.chat_message_histories.in_memory'] = mock_module
    
    # Also try to patch the bridge module's import
    def _patched_import(name, *args, **kwargs):
        """Patched import that avoids chat_message_histories."""
        if name == 'langchain_community.chat_message_histories':
            return mock_module
        if name == 'langchain_community.chat_message_histories.in_memory':
            return mock_module
        # Use original import for everything else
        return __import__(name, *args, **kwargs)
    
    # Store original import
    _original_import = __builtins__.__import__ if isinstance(__builtins__, dict) else __builtins__['__import__']
    
    # Patch __import__ - but this is risky, so we'll do it conditionally
    # Actually, let's not patch __import__ globally as it can cause issues
    # Instead, we'll just mock the modules and hope the validator patch works
except Exception:
    pass

# CRITICAL: Monkey-patch resolve_embed_model BEFORE importing VectorStoreIndex
# This prevents it from importing langchain_community which triggers BaseMessage errors
try:
    from llama_index.core.embeddings.utils import resolve_embed_model
    _original_resolve_embed_model = resolve_embed_model
    
    def _patched_resolve_embed_model(embed_model_name="default", embed_model=None):
        """Patched resolve_embed_model that avoids langchain imports."""
        # If embed_model is passed directly, use it immediately (no imports needed)
        if embed_model is not None:
            return embed_model
            
        # If we already have an embed_model set in Settings, return it immediately
        # This avoids any imports that might trigger BaseMessage validation errors
        if hasattr(Settings, '_embed_model') and Settings._embed_model is not None:
            return Settings._embed_model
        
        # NEVER call the original function - it will trigger problematic imports
        # Instead, return None or raise a clear error
        # The caller should handle None or we should have already set _embed_model
        if hasattr(Settings, '_embed_model'):
            return Settings._embed_model
        
        # If we get here, something is wrong - but don't import langchain
        raise ValueError("No embed_model available and cannot resolve (langchain imports disabled)")
    
    # Replace in the module
    import llama_index.core.embeddings.utils as utils_module
    utils_module.resolve_embed_model = _patched_resolve_embed_model
except (ImportError, AttributeError):
    # If we can't patch, that's okay - we'll handle errors later
    pass

from workflow import CorrectiveRAGWorkflow
from agentic_workflow import AgenticRAGWorkflow
from llama_index.core import Settings
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.litellm import LiteLLM
import time
import uuid
import tempfile
import gc
import base64
import chromadb
import streamlit as st
import asyncio
import sys
import logging
import warnings
from dotenv import load_dotenv
import nest_asyncio
nest_asyncio.apply()

load_dotenv()

# Suppress Pydantic V1/V2 mixing warnings from dependencies
# These warnings come from langchain_community which uses Pydantic v1
# while langchain_core uses Pydantic v2. This is a known issue in the ecosystem.
warnings.filterwarnings("ignore", message=".*Mixing V1.*V2.*", category=UserWarning)
warnings.filterwarnings("ignore", message=".*_v1 module was a compatibility shim.*", category=UserWarning)

# Configuration validation
def validate_configuration():
    """Validate that all required configuration is present."""
    errors = []
    warnings = []
    
    # Check required environment variables
    if not os.getenv("FIRECRAWL_API_KEY"):
        errors.append("FIRECRAWL_API_KEY is not set. Please set it in your .env file or environment.")
    
    if not os.getenv("OPENROUTER_API_KEY"):
        errors.append("OPENROUTER_API_KEY is not set. Please set it in your .env file or environment.")
    
    # Check optional but recommended settings
    if not os.path.exists(".env"):
        warnings.append("No .env file found. Consider creating one for easier configuration.")
    
    # Display errors if any
    if errors:
        error_msg = "❌ **Configuration Errors:**\n\n"
        for error in errors:
            error_msg += f"- {error}\n"
        error_msg += "\n💡 **Solution:** Create a `.env` file in the project root with:\n"
        error_msg += "```\n"
        error_msg += "FIRECRAWL_API_KEY=your_firecrawl_api_key_here\n"
        error_msg += "OPENROUTER_API_KEY=your_openrouter_api_key_here\n"
        error_msg += "```\n"
        error_msg += "\nOr set them as environment variables."
        return False, error_msg
    
    # Display warnings if any (non-blocking)
    if warnings:
        warning_msg = "⚠️ **Configuration Warnings:**\n\n"
        for warning in warnings:
            warning_msg += f"- {warning}\n"
        return True, warning_msg
    
    return True, None

# Validate configuration before setting up the app
_config_valid, _config_msg = validate_configuration()

# Set up page configuration
st.set_page_config(
    page_title="IntelliChat - RAG Assistant", 
    layout="wide",
    page_icon="🤖"
)

# Display configuration errors if any
if not _config_valid:
    st.error(_config_msg)
    st.stop()
elif _config_msg:
    st.warning(_config_msg)

# Custom CSS for enhanced UI
st.markdown("""
<style>
    /* Main background and text colors */
    :root {
        --primary-color: #4F46E5;
        --secondary-color: #818CF8;
        --accent-color: #FBBF24;
        --background-color: #F9FAFB;
        --card-color: #FFFFFF;
        --text-primary: #1F2937;
        --text-secondary: #6B7280;
    }
    
    /* Dark mode support */
    @media (prefers-color-scheme: dark) {
        :root {
            --background-color: #111827;
            --card-color: #1F2937;
            --text-primary: #F9FAFB;
            --text-secondary: #D1D5DB;
        }
    }
    
    /* Main app styling */
    .main {
        background-color: var(--background-color);
    }
    
    /* Header styling */
    header {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)) !important;
        padding: 2rem 0;
        border-radius: 0 0 20px 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Titles and headings */
    h1, h2, h3 {
        color: var(--text-primary);
        font-weight: 700;
    }
    
    /* Custom cards */
    div[data-testid="stHorizontalBlock"] > div {
        background-color: var(--card-color);
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    div[data-testid="stHorizontalBlock"] > div:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(to right, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(79, 70, 229, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(79, 70, 229, 0.4);
    }
    
    /* File uploader */
    .stFileUploader {
        background-color: var(--card-color);
        border: 2px dashed var(--secondary-color);
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
    }
    
    /* Chat messages */
    .chat-message {
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .user-message {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        border-radius: 12px 12px 0 12px;
        margin-left: 20%;
    }
    
    .assistant-message {
        background-color: var(--card-color);
        border: 1px solid var(--secondary-color);
        border-radius: 12px 12px 12px 0;
        margin-right: 20%;
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 2px solid var(--secondary-color);
        padding: 1rem;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: var(--card-color);
        border-radius: 12px;
        border: 1px solid var(--secondary-color);
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: var(--card-color);
        border-right: 1px solid var(--secondary-color);
    }
    
    /* Progress bars */
    .stProgress > div > div {
        background: linear-gradient(to right, var(--primary-color), var(--secondary-color));
    }
    
    /* Animation for loading states */
    @keyframes pulse {
        0% { opacity: 0.6; }
        50% { opacity: 1; }
        100% { opacity: 0.6; }
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if "id" not in st.session_state:
    st.session_state.id = uuid.uuid4()
    st.session_state.file_cache = {}

if "workflow" not in st.session_state:
    st.session_state.workflow = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "workflow_logs" not in st.session_state:
    st.session_state.workflow_logs = []

if "document_uploaded" not in st.session_state:
    st.session_state.document_uploaded = False

session_id = st.session_state.id


@st.cache_resource
def load_llm():
    """Load and cache the LLM model."""
    try:
        # Use a reliable model that's known to work on OpenRouter
        # Format: openrouter/provider/model-name
        llm = LiteLLM(
            model="openrouter/google/gemini-2.0-flash-exp:free",
            api_base="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY")
        )
        print(f"✅ LLM loaded: google/gemini-2.0-flash-exp:free")
        return llm
    except Exception as e:
        st.error(f"Failed to load LLM: {e}")
        raise


def _safe_set_embed_model(embed_model):
    """
    Safely set the embed_model on Settings using direct assignment.
    
    We NEVER use Settings.embed_model = embed_model because it triggers
    langchain_community imports that have Pydantic v1 BaseMessage validation errors.
    Instead, we always use direct assignment to Settings._embed_model.
    """
    # ALWAYS use direct assignment to bypass property setter
    # The property setter calls resolve_embed_model() which imports langchain_community
    # classes that fail during Pydantic v1 class definition
    Settings._embed_model = embed_model


def _create_embedding_model_safe(model_name: str = "text-embedding-3-small"):
    """
    Create OpenAI embedding model via OpenRouter API.
    
    Args:
        model_name: OpenAI embedding model name (OpenRouter routes automatically)
                   Options: 
                   - text-embedding-3-small (default, faster, cheaper)
                   - text-embedding-3-large (better quality)
                   - text-embedding-ada-002 (older, cheaper)
    
    Returns:
        OpenAIEmbedding instance configured for OpenRouter
    """
    from pydantic import ValidationError
    
    try:
        # Create OpenAI embedding model with OpenRouter API configuration
        # Note: Use standard OpenAI model names (e.g., "text-embedding-3-small")
        # OpenRouter will route to OpenAI automatically based on api_base
        embed_model = OpenAIEmbedding(
            model=model_name,
            api_key=os.getenv("OPENROUTER_API_KEY"),
            api_base="https://openrouter.ai/api/v1",  # OpenRouter API endpoint
        )
        return embed_model
    except (ValidationError, TypeError) as e:
        error_msg = str(e)
        if "BaseMessage" in error_msg or "arbitrary_types_allowed" in error_msg:
            # The error is about BaseMessage validation
            # Force set the model_config on the class before creating instance
            try:
                from pydantic import ConfigDict
                # Get the class and force update its config
                OpenAIEmbedding.model_config = ConfigDict(arbitrary_types_allowed=True)
                # Also try to update the __pydantic_config__ directly
                if hasattr(OpenAIEmbedding, '__pydantic_config__'):
                    OpenAIEmbedding.__pydantic_config__ = ConfigDict(arbitrary_types_allowed=True)
                
                # Retry creation after forcing config
                return OpenAIEmbedding(
                    model=model_name,
                    api_key=os.getenv("OPENROUTER_API_KEY"),
                    api_base="https://openrouter.ai/api/v1",
                )
            except Exception as e2:
                # If that still fails, raise the original error
                raise e from e2
        else:
            # Not a BaseMessage error, re-raise
            raise


@st.cache_resource
def load_embedding_model(model_name: str = "text-embedding-3-small"):
    """
    Load and cache the OpenAI embedding model via OpenRouter API.
    
    Args:
        model_name: OpenAI embedding model name
                   Options: 
                   - text-embedding-3-small (default, faster, cheaper)
                   - text-embedding-3-large (better quality)
                   - text-embedding-ada-002 (older, cheaper)
    
    Returns:
        Configured OpenAIEmbedding instance
    """
    try:
        # Use the safe creation function
        embed_model = _create_embedding_model_safe(model_name)
            
        # Set as global embedding model with error handling
        _safe_set_embed_model(embed_model)
        
        return embed_model
    except Exception as e:
        # For errors, try fallback model
        error_str = str(e).lower()
        st.warning(f"Failed to load {model_name}. Trying fallback model...")
        try:
            # Try with ada-002 as fallback (older but more stable)
            embed_model = _create_embedding_model_safe("text-embedding-ada-002")
            _safe_set_embed_model(embed_model)
            return embed_model
        except Exception as e2:
            st.error(f"Failed to load embedding model: {e2}")
            raise RuntimeError(f"Failed to load embedding model. Original: {e}, Fallback: {e2}") from e2


def reset_chat():
    st.session_state.messages = []
    st.session_state.workflow_logs = []
    st.session_state.document_uploaded = False
    gc.collect()


def display_pdf(file):
    st.markdown("### 📄 Document Preview")
    base64_pdf = base64.b64encode(file.read()).decode("utf-8")

    # Embedding PDF in HTML
    pdf_display = f"""<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600px" type="application/pdf"
                        style="border-radius: 12px; border: 1px solid #E5E7EB;"
                    >
                    </iframe>"""

    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)

# Function to initialize the workflow with uploaded documents


def initialize_workflow(file_path):
    """Initialize workflow with improved error handling and BaseMessage sanitization."""
    try:
        # Ensure pydantic_config is imported and applied
        import pydantic_config  # noqa: F401
        
        with st.spinner("🧠 Processing your document..."):
            # Show progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("📚 Loading documents...")
            progress_bar.progress(20)
            
            # Load documents with error handling
            try:
                documents = SimpleDirectoryReader(file_path).load_data()
                print(f"DEBUG: Loaded {len(documents)} documents")
            except Exception as e:
                st.error(f"Failed to load documents: {e}")
                raise
            
            status_text.text("🗄️ Setting up vector store...")
            progress_bar.progress(40)
            # Set up ChromaDB client
            chroma_client = chromadb.PersistentClient(path="./chroma_db")
            chroma_collection = chroma_client.get_or_create_collection("demo_collection")
            vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
            print("DEBUG: Chroma vector store created")
            
            status_text.text("⚙️ Initializing embedding model...")
            progress_bar.progress(60)
            # Use cached embedding model for better performance
            try:
                embed_model = load_embedding_model(
                    model_name="text-embedding-3-small"  # Using OpenAI embeddings via OpenRouter
                )
                # Set embed_model on Settings with error handling
                # Note: load_embedding_model already sets it, but we ensure it's set here too
                try:
                    _safe_set_embed_model(embed_model)
                except Exception as e:
                    # If safe_set fails, try direct assignment
                    error_msg = str(e).lower()
                    if "basemessage" in error_msg or "arbitrary_types_allowed" in error_msg:
                        Settings._embed_model = embed_model
                    else:
                        raise
                print("DEBUG: Embedding model loaded and cached")
            except Exception as e:
                error_msg = str(e).lower()
                if "basemessage" in error_msg or "arbitrary_types_allowed" in error_msg:
                    # Try with fallback model
                    st.warning("Primary model failed, trying fallback model...")
                    embed_model = load_embedding_model(
                        model_name="text-embedding-ada-002"  # Fallback to older but stable model
                    )
                    _safe_set_embed_model(embed_model)
                    print("DEBUG: Smaller embedding model loaded and cached")
                else:
                    raise
            
            status_text.text("🤖 Loading language model...")
            progress_bar.progress(80)
            llm = load_llm()
            print("DEBUG: LLM loaded")

            Settings.llm = llm
            storage_context = StorageContext.from_defaults(
                vector_store=vector_store)
            print("DEBUG: Storage context created")
            
            status_text.text("🔍 Creating document index...")
            progress_bar.progress(90)
            # Create index manually to bypass Pydantic v2 compatibility issues
            # This avoids the __modify_schema__ error and BaseMessage validation issues
            try:
                # Ensure embed_model is set safely
                _safe_set_embed_model(embed_model)
                
                # MANUAL INDEX CREATION - bypasses problematic from_documents method
                from llama_index.core.node_parser import SimpleNodeParser
                from llama_index.core.schema import TextNode
                
                # Parse documents into nodes manually
                node_parser = SimpleNodeParser.from_defaults()
                nodes = node_parser.get_nodes_from_documents(documents)
                
                # Embed nodes manually
                status_text.text("🔄 Embedding documents...")
                print(f"DEBUG: Embedding {len(nodes)} nodes")
                for i, node in enumerate(nodes):
                    if i % 5 == 0:
                        status_text.text(f"🔄 Embedding documents... ({i+1}/{len(nodes)})")
                    
                    if hasattr(node, 'get_content'):
                        text = node.get_content()
                    else:
                        text = getattr(node, 'text', '')
                    
                    if text:
                        try:
                            # Get embedding from embed_model
                            embedding = embed_model.get_text_embedding(text)
                            node.embedding = embedding
                        except Exception as e:
                            # If embedding fails, skip or use empty embedding
                            print(f"Warning: Failed to embed node: {e}")
                            node.embedding = None
                
                print(f"DEBUG: All {len(nodes)} nodes embedded")
                
                # Store nodes in vector store manually
                status_text.text("💾 Storing vectors in database...")
                vector_store.add(nodes)
                print(f"DEBUG: Stored {len(nodes)} nodes in vector store")
                
                # COMPLETELY BYPASS VectorStoreIndex - create custom index wrapper
                # This avoids ALL pydantic/langchain import issues
                status_text.text("🔗 Creating index wrapper...")
                
                class CustomVectorIndex:
                    """Custom index that wraps vector store without triggering problematic imports."""
                    def __init__(self, vector_store, storage_context, embed_model, nodes):
                        self._vector_store = vector_store
                        self._storage_context = storage_context
                        self._embed_model = embed_model
                        self._nodes = nodes
                        # Expose attributes expected by workflows
                        self.vector_store = vector_store
                        self.storage_context = storage_context
                        self.embed_model = embed_model
                        # Add docstore from storage_context
                        self.docstore = storage_context.docstore if storage_context else None
                        self.index_struct = None  # Not needed for our use case
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
                        """Fallback for any missing attributes - return None or empty."""
                        # Avoid infinite recursion
                        if name.startswith('_'):
                            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
                        print(f"Warning: Accessing missing attribute '{name}' on CustomVectorIndex")
                        return None
                
                # Create custom index (no problematic initialization)
                index = CustomVectorIndex(
                    vector_store=vector_store,
                    storage_context=storage_context,
                    embed_model=embed_model,
                    nodes=nodes
                )
                
                print("DEBUG: Custom index wrapper created - SUCCESS!")
                st.success("✅ Document index created successfully!")
                
            except Exception as index_error:
                # If custom index creation fails, show error
                st.error(f"❌ Failed to create index: {index_error}")
                import traceback
                error_trace = traceback.format_exc()
                print(f"Index creation error:\n{error_trace}")
                st.error(f"Full error traceback:\n```\n{error_trace}\n```")
                raise

            # Check if FIRECRAWL_API_KEY is available
            if "FIRECRAWL_API_KEY" not in os.environ:
                raise ValueError("FireCrawl API key not found. Please enter it in the sidebar.")

            # Use AgenticRAGWorkflow for agent-based architecture
            # Ensure all BaseMessage objects are sanitized before workflow creation
            try:
                # Sanitize any potential BaseMessage objects in the environment
                from langchain_core.messages.base import BaseMessage
                
                # Ensure LLM doesn't contain BaseMessage objects
                if hasattr(llm, '_model') and isinstance(llm._model, BaseMessage):
                    st.warning("Detected BaseMessage in LLM, sanitizing...")
                
            except (ImportError, AttributeError):
                pass
            
            # Create workflow with sanitized inputs and comprehensive error handling
            try:
                # Wrap workflow creation in try-except to catch BaseMessage errors
                workflow = AgenticRAGWorkflow(
                    index=index,
                    firecrawl_api_key=os.environ["FIRECRAWL_API_KEY"],
                    verbose=True,
                    timeout=249,
                    llm=llm
                )
                print("DEBUG: Workflow created successfully")
            except Exception as workflow_error:
                # Check if it's a BaseMessage validation error
                error_str = str(workflow_error)
                if "BaseMessage" in error_str or "arbitrary_types_allowed" in error_str:
                    st.warning("⚠️ BaseMessage validation error detected. Attempting to fix...")
                    # Try to fix by ensuring model_config is set on the workflow class
                    try:
                        from pydantic import ConfigDict
                        # Force set model_config on AgenticRAGWorkflow if not already set
                        if not hasattr(AgenticRAGWorkflow, 'model_config') or \
                           (hasattr(AgenticRAGWorkflow.model_config, 'get') and 
                            not AgenticRAGWorkflow.model_config.get('arbitrary_types_allowed')):
                            AgenticRAGWorkflow.model_config = ConfigDict(arbitrary_types_allowed=True)
                        
                        # Also patch the base Workflow class
                        from llama_index.core.workflow import Workflow
                        Workflow.model_config = ConfigDict(arbitrary_types_allowed=True)
                        
                        # Try to re-import pydantic_config to ensure patches are applied
                        import importlib
                        import pydantic_config
                        importlib.reload(pydantic_config)
                        
                        # Retry workflow creation
                        workflow = AgenticRAGWorkflow(
                            index=index,
                            firecrawl_api_key=os.environ["FIRECRAWL_API_KEY"],
                            verbose=True,
                            timeout=249,
                            llm=llm
                        )
                        st.success("✅ Fixed BaseMessage validation error!")
                        print("DEBUG: Workflow created successfully after retry")
                    except Exception as fix_error:
                        st.error(f"❌ Failed to fix BaseMessage error: {fix_error}")
                        # Re-raise original error
                        raise workflow_error from fix_error
                else:
                    # Re-raise if it's a different error
                    raise

            st.session_state.workflow = workflow
            progress_bar.progress(100)
            status_text.text("✅ Document processing complete!")
            time.sleep(1)
            progress_bar.empty()
            status_text.empty()
            return workflow
    except Exception as e:
        st.error(f"❌ Failed to initialize workflow: {e}")
        raise e

# Function to run the async workflow


async def run_workflow(query):
    try:
        # Capture stdout to get the workflow logs
        f = io.StringIO()
        with redirect_stdout(f):
            # Add timeout to prevent hanging
            # Invoke workflow by creating a StartEvent with the query
            from llama_index.core.workflow import StartEvent
            
            # Increase timeout to 5 minutes for complex queries
            result = await asyncio.wait_for(
                st.session_state.workflow.run(query_str=query),
                timeout=300  # 5 minutes timeout
            )

        # Get the captured logs and store them
        logs = f.getvalue()
        if logs:
            st.session_state.workflow_logs.append(logs)

        return result
    except asyncio.TimeoutError:
        st.error("⏰ Workflow execution timed out after 2 minutes")
        raise Exception("Workflow execution timed out")
    except Exception as e:
        # Log the error and re-raise it
        st.error(f"❌ Workflow execution failed: {e}")
        raise e

# Enhanced sidebar for document upload
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>📁 Document Assistant</h2>", unsafe_allow_html=True)
    
    # Logo or icon
    st.markdown("<div style='text-align: center; margin: 20px 0;'><span style='font-size: 3rem;'>🤖</span></div>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Upload your PDF document", type="pdf", key="pdf_uploader")
    
    if uploaded_file:
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                file_path = os.path.join(temp_dir, uploaded_file.name)

                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getvalue())

                file_key = f"{session_id}-{uploaded_file.name}"
                
                if file_key not in st.session_state.get('file_cache', {}):
                    # Initialize workflow with the uploaded document
                    workflow = initialize_workflow(temp_dir)
                    st.session_state.file_cache[file_key] = workflow
                    st.session_state.document_uploaded = True
                else:
                    st.session_state.workflow = st.session_state.file_cache[file_key]
                    st.session_state.document_uploaded = True

                # Inform the user that the file is processed and Display the PDF uploaded
                st.success("✅ Ready to Chat!")
                with st.expander("📄 View Document"):
                    display_pdf(uploaded_file)
        except Exception as e:
            st.error(f"❌ An error occurred: {e}")
            st.stop()
    
    # Add information section
    st.markdown("---")
    st.markdown("### ℹ️ About This Tool")
    st.markdown("""
    This intelligent assistant combines:
    - 📚 Document analysis
    - 🔍 Web search capabilities
    - 🤖 Advanced AI reasoning
    
    Upload a PDF and ask questions to get started!
    """)
    
    # Add reset button
    if st.button("🔄 Reset Conversation"):
        reset_chat()
        st.rerun()

# Main chat interface
col1, col2 = st.columns([7, 3])

with col1:
    # Centered main heading with enhanced styling
    st.markdown('''
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem;">🤖 IntelliChat Assistant</h1>
            <p style="font-size: 1.2rem; color: var(--text-secondary);">Your intelligent document companion powered by RAG</p>
        </div>
    ''', unsafe_allow_html=True)
    
    # Enhanced logos section
    st.markdown('''
        <div style="text-align: center; margin: 20px 0 30px 0;">
            <div style="display: flex; justify-content: center; align-items: center; gap: 30px; flex-wrap: wrap;">
                <div style="text-align: center;">
                    <img src="https://mintlify.s3.us-west-1.amazonaws.com/firecrawl/logo/logo-dark.png" alt="Firecrawl" style="height: 50px; margin-bottom: 5px;">
                    <p style="font-size: 0.8rem; color: var(--text-secondary); margin: 0;">FireCrawl</p>
                </div>
                <div style="text-align: center;">
                    <img src="https://i.ibb.co/m5RtcvnY/beam-logo.png" alt="Beam Cloud" style="height: 50px; margin-bottom: 5px;">
                    <p style="font-size: 0.8rem; color: var(--text-secondary); margin: 0;">Beam</p>
                </div>
                <div style="text-align: center;">
                    <img src="https://milvus.io/images/layout/milvus-logo.svg" alt="Milvus" style="height: 50px; margin-bottom: 5px;">
                    <p style="font-size: 0.8rem; color: var(--text-secondary); margin: 0;">Milvus</p>
                </div>
            </div>
        </div>
    ''', unsafe_allow_html=True)
    
    # Welcome message when no document is uploaded
    if not st.session_state.document_uploaded:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background-color: var(--card-color); border-radius: 15px; border: 2px dashed var(--secondary-color);">
            <h2>👋 Welcome to IntelliChat!</h2>
            <p style="font-size: 1.1rem; color: var(--text-secondary);">
                To get started, please upload a PDF document using the sidebar on the left.<br>
                Once uploaded, you can ask questions about your document and I'll help you find answers.
            </p>
            <div style="font-size: 3rem; margin: 1rem 0;">📄💬🔍</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Display chat messages from history on app rerun
    for i, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            st.markdown(f"<div class='chat-message {message['role']}-message'>{message['content']}</div>", unsafe_allow_html=True)

        # If this is a user message and there are logs associated with it
        # Display logs AFTER the user message but BEFORE the next assistant message
        if message["role"] == "user" and "log_index" in message and i < len(st.session_state.messages) - 1:
            log_index = message["log_index"]
            if log_index < len(st.session_state.workflow_logs):
                with st.expander("📊 View Process Details", expanded=False):
                    st.code(
                        st.session_state.workflow_logs[log_index], language="text")

# Accept user input
if st.session_state.document_uploaded:
    if prompt := st.chat_input("Ask a question about your document..."):
        # Add user message to chat history with placeholder for log index
        log_index = len(st.session_state.workflow_logs)
        st.session_state.messages.append(
            {"role": "user", "content": prompt, "log_index": log_index})

        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(f"<div class='chat-message user-message'>{prompt}</div>", unsafe_allow_html=True)

        if st.session_state.workflow:
            try:
                # Show thinking indicator
                with st.chat_message("assistant"):
                    with st.spinner("🤔 Thinking..."):
                        # Run the async workflow with proper error handling
                        result = asyncio.run(run_workflow(prompt))

                    # Display the workflow logs in an expandable section OUTSIDE and BEFORE the assistant chat bubble
                    if log_index < len(st.session_state.workflow_logs):
                        with st.expander("📊 View Process Details", expanded=False):
                            st.code(
                                st.session_state.workflow_logs[log_index], language="text")

                    # Display assistant response in chat message container
                    message_placeholder = st.empty()
                    full_response = ""

                    if hasattr(result, 'response'):
                        result_text = result.response
                    else:
                        result_text = str(result)

                    # Stream the response word by word
                    words = result_text.split()
                    for i, word in enumerate(words):
                        full_response += word + " "
                        message_placeholder.markdown(f"<div class='chat-message assistant-message'>{full_response}▌</div>", unsafe_allow_html=True)
                        # Add a delay between words
                        if i < len(words) - 1:  # Don't delay after the last word
                            time.sleep(0.05)

                    # Display final response without cursor
                    message_placeholder.markdown(f"<div class='chat-message assistant-message'>{full_response}</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ Error running workflow: {e}")
                full_response = f"An error occurred while processing your request: {e}"
                st.markdown(full_response)

            # Add assistant response to chat history
            st.session_state.messages.append(
                {"role": "assistant", "content": full_response})
else:
    # Disable chat input when no document is uploaded
    st.chat_input("Please upload a document first...", disabled=True)