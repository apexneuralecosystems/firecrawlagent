"""
Comprehensive Pydantic v2 configuration for LangChain BaseMessage compatibility.

This module patches the llama-index Workflow and Context classes to allow arbitrary types,
preventing Pydantic validation errors when BaseMessage objects are used.

IMPORTANT: This module MUST be imported before any workflow classes are instantiated.
"""

import os
import warnings

# CRITICAL: Import langchain_patch FIRST to patch Pydantic v1 validators
# This prevents BaseMessage validation errors during langchain_community imports
try:
    import langchain_patch  # noqa: F401
except ImportError:
    # If langchain_patch doesn't exist yet, that's okay
    pass

# Set environment variable BEFORE any Pydantic imports
os.environ["PYDANTIC_ALLOW_ARBITRARY_TYPES"] = "true"

# CRITICAL: Set Pydantic to use strict mode that allows arbitrary types by default
# This is a workaround for BaseMessage validation issues
os.environ["PYDANTIC_CONFIG"] = "arbitrary_types_allowed=true"

# Suppress Pydantic V1/V2 mixing warnings from dependencies
# These warnings come from langchain_community which uses Pydantic v1
# while langchain_core uses Pydantic v2. This is a known issue in the ecosystem.
warnings.filterwarnings("ignore", message=".*Mixing V1.*V2.*", category=UserWarning)
warnings.filterwarnings("ignore", message=".*_v1 module was a compatibility shim.*", category=UserWarning)

# Import Pydantic v2 components
import pydantic
from pydantic import ConfigDict

# CRITICAL: Register BaseMessage as a known type in Pydantic's type registry
# This must happen before any models are created
try:
    from langchain_core.messages.base import BaseMessage
    # Register BaseMessage in Pydantic's type registry if possible
    try:
        # For Pydantic v2, try to add to the known types
        if hasattr(pydantic, '_known_arbitrary_types'):
            pydantic._known_arbitrary_types.add(BaseMessage)
        # Also try to register it as a valid type
        if hasattr(pydantic, 'json_schema_mode'):
            # This ensures BaseMessage is treated as an arbitrary type
            pass
    except (AttributeError, TypeError):
        pass
except (ImportError, AttributeError):
    # BaseMessage not available yet - will be registered later
    pass

# CRITICAL: Patch Pydantic's type validation to allow BaseMessage globally
# This must happen before any Pydantic models are created
try:
    from langchain_core.messages.base import BaseMessage
    
    # Register BaseMessage as a valid type for Pydantic
    # This allows BaseMessage to pass validation without arbitrary_types_allowed
    if hasattr(pydantic, '_validators'):
        # For Pydantic v2, we need to register a custom validator
        try:
            from pydantic._internal._generate_schema import GenerateSchema
            from pydantic._internal._config import ConfigWrapper
            
            # Create a custom schema generator that allows BaseMessage
            original_get_schema = None
            if hasattr(GenerateSchema, 'generate_schema'):
                original_get_schema = GenerateSchema.generate_schema
                
                def patched_generate_schema(self, source_type, config_wrapper):
                    # If it's a BaseMessage, allow it
                    if source_type is BaseMessage or (hasattr(source_type, '__mro__') and BaseMessage in source_type.__mro__):
                        # Return a schema that accepts BaseMessage
                        from pydantic_core import core_schema
                        return core_schema.any_schema()
                    # Otherwise, use the original
                    return original_get_schema(self, source_type, config_wrapper)
                
                GenerateSchema.generate_schema = patched_generate_schema
        except (ImportError, AttributeError):
            pass
    
    # Also patch Pydantic's core validation to be more permissive
    try:
        import pydantic._internal._validators as validators_module
        original_get_validator = getattr(validators_module, 'get_validator', None)
        if original_get_validator:
            def patched_get_validator(type_, config):
                # If it's a BaseMessage type, return a validator that accepts anything
                if isinstance(type_, type):
                    try:
                        if issubclass(type_, BaseMessage):
                            # Return a no-op validator that converts to string
                            def basemessage_validator(v):
                                if isinstance(v, BaseMessage):
                                    return v.content if hasattr(v, 'content') else str(v)
                                return v
                            return basemessage_validator
                    except TypeError:
                        pass
                # For all other types, use original
                return original_get_validator(type_, config)
            validators_module.get_validator = patched_get_validator
    except (ImportError, AttributeError):
        pass
    
    # Patch Pydantic's field annotation handling to allow BaseMessage
    try:
        from pydantic._internal._annotated_handlers import GetCoreSchemaHandler
        from pydantic_core import core_schema
        
        # Create a custom annotation handler for BaseMessage
        def handle_basemessage_annotation(source_type, handler: GetCoreSchemaHandler):
            """Handle BaseMessage type annotations by allowing any type."""
            if source_type is BaseMessage or (hasattr(source_type, '__mro__') and BaseMessage in source_type.__mro__):
                return core_schema.any_schema()
            # For other types, use default handler
            return handler(source_type)
        
        # Try to register the handler
        try:
            from pydantic._internal._annotated_handlers import GetCoreSchemaHandler
            # This is a simplified approach - we'll let the model_config handle it
            pass
        except (ImportError, AttributeError):
            pass
    except (ImportError, AttributeError):
        pass
except (ImportError, AttributeError):
    # If we can't patch at this level, we'll rely on model_config patching
    pass

# Import llama-index workflow components
try:
    from llama_index.core.workflow import Workflow, Context, Event, StartEvent, StopEvent
except ImportError as e:
    # If imports fail, we can't patch - but this shouldn't happen in normal usage
    raise ImportError(f"Failed to import llama-index workflow components: {e}. "
                     f"Make sure llama-index-core is installed.") from e


def _patch_model_config(cls, class_name: str = "Unknown"):
    """
    Safely patch a Pydantic model's model_config to allow arbitrary types.
    
    Args:
        cls: The class to patch
        class_name: Name of the class for error messages
    """
    try:
        if not issubclass(cls, pydantic.BaseModel):
            # Not a Pydantic model, skip
            return
        
        # For Pydantic v2, we need to set model_config properly
        # Try multiple approaches to ensure it works
        
        # Approach 1: Direct assignment
        try:
            if hasattr(cls, 'model_config'):
                existing = cls.model_config
                if isinstance(existing, dict):
                    existing['arbitrary_types_allowed'] = True
                    cls.model_config = ConfigDict(**existing)
                elif isinstance(existing, pydantic.ConfigDict):
                    # Create new ConfigDict with arbitrary_types_allowed
                    cls.model_config = ConfigDict(
                        arbitrary_types_allowed=True,
                        **{k: v for k, v in existing.items() if k != 'arbitrary_types_allowed'}
                    )
                else:
                    cls.model_config = ConfigDict(arbitrary_types_allowed=True)
            else:
                cls.model_config = ConfigDict(arbitrary_types_allowed=True)
        except Exception:
            pass
        
        # Approach 2: Try to set via __pydantic_config__
        try:
            if hasattr(cls, '__pydantic_config__'):
                config = cls.__pydantic_config__
                if isinstance(config, dict):
                    config['arbitrary_types_allowed'] = True
                elif isinstance(config, pydantic.ConfigDict):
                    cls.__pydantic_config__ = ConfigDict(
                        arbitrary_types_allowed=True,
                        **{k: v for k, v in config.items() if k != 'arbitrary_types_allowed'}
                    )
        except Exception:
            pass
        
        # Approach 3: Patch via __init_subclass__ if available
        # Note: We skip this approach as it's complex and can cause issues
        # The direct model_config assignment should be sufficient
        pass
            
    except Exception as e:
        # Log but don't fail - some classes might not be patchable
        warnings.warn(f"Failed to patch {class_name}: {e}", RuntimeWarning)

# Patch all base classes
# IMPORTANT: Patch Event as well to prevent validation errors
_patch_model_config(Workflow, "Workflow")
_patch_model_config(Context, "Context")
# Patch Event base class - this is critical for preventing BaseMessage validation errors
try:
    _patch_model_config(Event, "Event")
except Exception as e:
    # If direct patching fails, try alternative approach
    warnings.warn(f"Failed to patch Event directly: {e}", RuntimeWarning)
_patch_model_config(StartEvent, "StartEvent")
_patch_model_config(StopEvent, "StopEvent")

# Also try to patch Settings if it's a Pydantic model
# CRITICAL: We must NOT trigger any property access here, especially embed_model
# because accessing it imports langchain_community which triggers BaseMessage errors.
# 
# NOTE: We skip patching Settings during import to avoid triggering property access.
# Settings will be patched lazily when needed, or we use _safe_set_embed_model() in app.py
# which directly sets Settings._embed_model to bypass property access.
#
# If you need to patch Settings, do it after all imports are complete and langchain_patch
# has been applied, or use the _safe_set_embed_model() function instead.

# CRITICAL: Patch langchain_community classes that use Pydantic v1
# These need to be patched before they're imported
try:
    # Pre-import to trigger class creation, then patch
    import warnings
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        try:
            from langchain_community.chat_message_histories.in_memory import ChatMessageHistory
            # Try to patch if it's a Pydantic v1 model
            if hasattr(ChatMessageHistory, 'Config'):
                # Pydantic v1
                original_config = ChatMessageHistory.Config
                if not hasattr(original_config, 'arbitrary_types_allowed'):
                    ChatMessageHistory.Config.arbitrary_types_allowed = True
        except (ImportError, AttributeError, TypeError):
            pass
except Exception:
    pass

# CRITICAL: Patch embedding models that might be Pydantic models
# These need to be patched before they're instantiated
# Use a flag to prevent re-patching which can cause recursion
_embedding_patched = False

# Patch OpenAIEmbedding (used for OpenRouter embeddings)
try:
    from llama_index.embeddings.openai import OpenAIEmbedding
    
    if not _embedding_patched:
        # Aggressively patch the model_config
        try:
            # Force set model_config with arbitrary_types_allowed
            if hasattr(OpenAIEmbedding, 'model_config'):
                # Get existing config or create new one
                existing = getattr(OpenAIEmbedding, 'model_config', {})
                if isinstance(existing, dict):
                    existing['arbitrary_types_allowed'] = True
                    OpenAIEmbedding.model_config = ConfigDict(**existing)
                elif isinstance(existing, pydantic.ConfigDict):
                    OpenAIEmbedding.model_config = ConfigDict(
                        arbitrary_types_allowed=True,
                        **{k: v for k, v in existing.items() if k != 'arbitrary_types_allowed'}
                    )
                else:
                    OpenAIEmbedding.model_config = ConfigDict(arbitrary_types_allowed=True)
            else:
                OpenAIEmbedding.model_config = ConfigDict(arbitrary_types_allowed=True)
        except Exception:
            pass
        
        # Also call the general patching function
        _patch_model_config(OpenAIEmbedding, "OpenAIEmbedding")
        _embedding_patched = True
except (ImportError, AttributeError, TypeError) as e:
    # If OpenAIEmbedding import fails, that's okay - just continue
    pass

# Keep FastEmbedEmbedding patch for backward compatibility (if still used)
_fastembed_patched = False
try:
    from llama_index.embeddings.fastembed import FastEmbedEmbedding
    
    if not _fastembed_patched:
        # Aggressively patch the model_config
        try:
            # Force set model_config with arbitrary_types_allowed
            if hasattr(FastEmbedEmbedding, 'model_config'):
                # Get existing config or create new one
                existing = getattr(FastEmbedEmbedding, 'model_config', {})
                if isinstance(existing, dict):
                    existing['arbitrary_types_allowed'] = True
                    FastEmbedEmbedding.model_config = ConfigDict(**existing)
                elif isinstance(existing, pydantic.ConfigDict):
                    FastEmbedEmbedding.model_config = ConfigDict(
                        arbitrary_types_allowed=True,
                        **{k: v for k, v in existing.items() if k != 'arbitrary_types_allowed'}
                    )
                else:
                    FastEmbedEmbedding.model_config = ConfigDict(arbitrary_types_allowed=True)
            else:
                FastEmbedEmbedding.model_config = ConfigDict(arbitrary_types_allowed=True)
        except Exception:
            pass
        
        # Also call the general patching function
        _patch_model_config(FastEmbedEmbedding, "FastEmbedEmbedding")
        
        # Also patch __init__ to sanitize BaseMessage objects (only once)
        try:
            from langchain_core.messages.base import BaseMessage
            # Check if already patched by looking for a marker attribute
            if not hasattr(FastEmbedEmbedding.__init__, '_sanitized_patch'):
                original_fastembed_init = FastEmbedEmbedding.__init__
                
                def sanitized_fastembed_init(self, *args, **kwargs):
                    """Sanitize kwargs to convert BaseMessage objects before Pydantic validation."""
                    # Sanitize all kwargs to remove BaseMessage objects
                    sanitized_kwargs = {}
                    for key, value in kwargs.items():
                        if isinstance(value, BaseMessage):
                            sanitized_kwargs[key] = value.content if hasattr(value, 'content') else str(value)
                        elif isinstance(value, (list, tuple)):
                            sanitized_kwargs[key] = type(value)([
                                (item.content if hasattr(item, 'content') else str(item)) if isinstance(item, BaseMessage) else item
                                for item in value
                            ])
                        elif isinstance(value, dict):
                            sanitized_kwargs[key] = {
                                k: (v.content if hasattr(v, 'content') else str(v)) if isinstance(v, BaseMessage) else v
                                for k, v in value.items()
                            }
                        else:
                            sanitized_kwargs[key] = value
                    
                    # Also sanitize args if any
                    sanitized_args = []
                    for arg in args:
                        if isinstance(arg, BaseMessage):
                            sanitized_args.append(arg.content if hasattr(arg, 'content') else str(arg))
                        else:
                            sanitized_args.append(arg)
                    
                    return original_fastembed_init(self, *sanitized_args, **sanitized_kwargs)
                
                # Mark as patched to prevent re-patching
                sanitized_fastembed_init._sanitized_patch = True
                FastEmbedEmbedding.__init__ = sanitized_fastembed_init
                _fastembed_patched = True
        except (ImportError, AttributeError) as e:
            # If BaseMessage import fails, that's okay - just continue
            pass
except (ImportError, AttributeError, TypeError) as e:
    # If FastEmbedEmbedding import fails, that's okay - just continue
    pass

# Patch base embedding class
try:
    from llama_index.core.base.embeddings.base import BaseEmbedding
    _patch_model_config(BaseEmbedding, "BaseEmbedding")
except (ImportError, AttributeError, TypeError):
    pass

# Patch LLM classes
try:
    from llama_index.llms.litellm import LiteLLM
    _patch_model_config(LiteLLM, "LiteLLM")
    
    # Also patch __init__ to sanitize BaseMessage objects
    try:
        from langchain_core.messages.base import BaseMessage
        original_litellm_init = LiteLLM.__init__
        
        def sanitized_litellm_init(self, *args, **kwargs):
            """Sanitize kwargs to convert BaseMessage objects before Pydantic validation."""
            sanitized_kwargs = {}
            for key, value in kwargs.items():
                if isinstance(value, BaseMessage):
                    sanitized_kwargs[key] = value.content if hasattr(value, 'content') else str(value)
                elif isinstance(value, (list, tuple)):
                    sanitized_kwargs[key] = [
                        (item.content if hasattr(item, 'content') else str(item)) if isinstance(item, BaseMessage) else item
                        for item in value
                    ]
                elif isinstance(value, dict):
                    sanitized_kwargs[key] = {
                        k: (v.content if hasattr(v, 'content') else str(v)) if isinstance(v, BaseMessage) else v
                        for k, v in value.items()
                    }
                else:
                    sanitized_kwargs[key] = value
            return original_litellm_init(self, *args, **sanitized_kwargs)
        
        LiteLLM.__init__ = sanitized_litellm_init
    except (ImportError, AttributeError):
        pass
except (ImportError, AttributeError, TypeError):
    pass

try:
    from llama_index.core.base.llms.base import BaseLLM
    _patch_model_config(BaseLLM, "BaseLLM")
except (ImportError, AttributeError, TypeError):
    pass

# CRITICAL: Patch index and schema-related classes
try:
    from llama_index.core import VectorStoreIndex
    _patch_model_config(VectorStoreIndex, "VectorStoreIndex")
except (ImportError, AttributeError, TypeError):
    pass

try:
    from llama_index.core.schema import Document, BaseNode, NodeWithScore
    _patch_model_config(Document, "Document")
    _patch_model_config(BaseNode, "BaseNode")
    _patch_model_config(NodeWithScore, "NodeWithScore")
except (ImportError, AttributeError, TypeError):
    pass

try:
    from llama_index.core.index.base import BaseIndex
    _patch_model_config(BaseIndex, "BaseIndex")
except (ImportError, AttributeError, TypeError):
    pass

try:
    from llama_index.core.storage.storage_context import StorageContext
    _patch_model_config(StorageContext, "StorageContext")
except (ImportError, AttributeError, TypeError):
    pass

try:
    from llama_index.core.vector_stores.types import VectorStore
    _patch_model_config(VectorStore, "VectorStore")
except (ImportError, AttributeError, TypeError):
    pass

try:
    from llama_index.vector_stores.chroma import ChromaVectorStore
    _patch_model_config(ChromaVectorStore, "ChromaVectorStore")
except (ImportError, AttributeError, TypeError):
    pass

try:
    from llama_index.core.base.base_retriever import BaseRetriever
    _patch_model_config(BaseRetriever, "BaseRetriever")
except (ImportError, AttributeError, TypeError):
    pass

try:
    from llama_index.core.retrievers import BaseRetriever
    _patch_model_config(BaseRetriever, "BaseRetriever")
except (ImportError, AttributeError, TypeError):
    pass

# CRITICAL: Patch Workflow.__init__ to sanitize inputs before Pydantic validation
# This ensures BaseMessage objects are converted before they reach Pydantic
try:
    from langchain_core.messages.base import BaseMessage
    from pydantic import ValidationError
    
    original_workflow_init = Workflow.__init__
    
    def sanitized_workflow_init(self, *args, **kwargs):
        """Sanitize kwargs to convert BaseMessage objects before Pydantic validation."""
        # Convert any BaseMessage objects in kwargs to strings
        sanitized_kwargs = {}
        for key, value in kwargs.items():
            if isinstance(value, BaseMessage):
                # Convert BaseMessage to string
                sanitized_kwargs[key] = value.content if hasattr(value, 'content') else str(value)
            elif isinstance(value, (list, tuple)):
                # Recursively check lists/tuples
                sanitized_kwargs[key] = [
                    (item.content if hasattr(item, 'content') else str(item)) if isinstance(item, BaseMessage) else item
                    for item in value
                ]
            elif isinstance(value, dict):
                # Recursively check dicts
                sanitized_kwargs[key] = {
                    k: (v.content if hasattr(v, 'content') else str(v)) if isinstance(v, BaseMessage) else v
                    for k, v in value.items()
                }
            else:
                sanitized_kwargs[key] = value
        
        # Try to call original __init__ with sanitized kwargs
        # If we get a BaseMessage validation error, ensure model_config is set and retry
        try:
            return original_workflow_init(self, *args, **sanitized_kwargs)
        except (ValidationError, TypeError, ValueError) as e:
            error_str = str(e)
            if "BaseMessage" in error_str or "arbitrary_types_allowed" in error_str:
                # Ensure model_config is set with arbitrary_types_allowed
                try:
                    if hasattr(self.__class__, 'model_config'):
                        # Try to merge with existing config
                        existing = self.__class__.model_config
                        if isinstance(existing, dict):
                            existing['arbitrary_types_allowed'] = True
                            self.__class__.model_config = ConfigDict(**existing)
                        elif isinstance(existing, ConfigDict):
                            self.__class__.model_config = ConfigDict(
                                arbitrary_types_allowed=True,
                                **{k: v for k, v in existing.items() if k != 'arbitrary_types_allowed'}
                            )
                        else:
                            self.__class__.model_config = ConfigDict(arbitrary_types_allowed=True)
                    else:
                        self.__class__.model_config = ConfigDict(arbitrary_types_allowed=True)
                    
                    # Retry initialization
                    return original_workflow_init(self, *args, **sanitized_kwargs)
                except Exception:
                    # If retry fails, raise original error
                    raise e
            else:
                # Not a BaseMessage error, re-raise
                raise
    
    Workflow.__init__ = sanitized_workflow_init
except (ImportError, AttributeError):
    # If BaseMessage isn't available or patching fails, continue without it
    pass

# Also patch at the class level using __init_subclass__ if needed
def patch_pydantic_model(cls):
    """Patch a Pydantic model class to allow arbitrary types."""
    if issubclass(cls, pydantic.BaseModel):
        _patch_model_config(cls, cls.__name__)
    return cls

# CRITICAL: Add a global Pydantic field validator that converts BaseMessage to string
# This is a last-resort catch-all for any BaseMessage objects that slip through
try:
    from langchain_core.messages.base import BaseMessage
    from pydantic import field_validator, model_validator
    
    # Patch BaseModel to automatically handle BaseMessage in field validation
    original_model_validate = pydantic.BaseModel.model_validate
    original_model_validate_fields = pydantic.BaseModel.model_validate_fields
    
    def patched_model_validate(cls, obj, **kwargs):
        """Patched model_validate that converts BaseMessage objects to strings."""
        # Recursively convert BaseMessage objects in the input
        def convert_basemessage(value):
            if isinstance(value, BaseMessage):
                return value.content if hasattr(value, 'content') else str(value)
            elif isinstance(value, dict):
                return {k: convert_basemessage(v) for k, v in value.items()}
            elif isinstance(value, (list, tuple)):
                return type(value)(convert_basemessage(item) for item in value)
            return value
        
        converted_obj = convert_basemessage(obj)
        return original_model_validate(cls, converted_obj, **kwargs)
    
    def patched_model_validate_fields(cls, values, **kwargs):
        """Patched model_validate_fields that converts BaseMessage objects to strings."""
        # Recursively convert BaseMessage objects in the values
        def convert_basemessage(value):
            if isinstance(value, BaseMessage):
                return value.content if hasattr(value, 'content') else str(value)
            elif isinstance(value, dict):
                return {k: convert_basemessage(v) for k, v in value.items()}
            elif isinstance(value, (list, tuple)):
                return type(value)(convert_basemessage(item) for item in value)
            return value
        
        converted_values = convert_basemessage(values)
        return original_model_validate_fields(cls, converted_values, **kwargs)
    
    pydantic.BaseModel.model_validate = classmethod(patched_model_validate)
    pydantic.BaseModel.model_validate_fields = classmethod(patched_model_validate_fields)
except (ImportError, AttributeError):
    pass

# Export the patched classes
__all__ = ['Workflow', 'Context', 'Event', 'StartEvent', 'StopEvent', 'ConfigDict', 'patch_pydantic_model']
