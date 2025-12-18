"""
Pre-import patching for langchain_community Pydantic v1 classes.
This must be imported BEFORE any llama_index code that triggers langchain_community imports.
"""
import os
import warnings

# Set environment variable
os.environ["PYDANTIC_ALLOW_ARBITRARY_TYPES"] = "true"

# Suppress warnings during patching
warnings.filterwarnings("ignore")

# CRITICAL: Patch Pydantic v1 validator to allow BaseMessage BEFORE any imports
# This must happen before ANY code tries to import langchain_community modules
try:
    import pydantic.v1.validators as pydantic_v1_validators
    
    # Store original find_validators BEFORE patching
    # Don't import langchain_core here - it might trigger the problematic imports!
    _original_find_validators = getattr(pydantic_v1_validators, 'find_validators', None)
    
    def patched_find_validators(type_, model_config):
        """Patched find_validators that allows BaseMessage types."""
        # CRITICAL: Check for BaseMessage FIRST, before calling original validator
        # This prevents the RuntimeError from being raised
        
        # ALWAYS enable arbitrary_types_allowed in model_config FIRST
        # This is the key - we need to set it before validation happens
        try:
            if hasattr(model_config, '__dict__'):
                model_config.__dict__['arbitrary_types_allowed'] = True
            if hasattr(model_config, 'arbitrary_types_allowed'):
                setattr(model_config, 'arbitrary_types_allowed', True)
            # Also try to set it on the class
            if hasattr(model_config, '__class__'):
                config_cls = model_config.__class__
                if hasattr(config_cls, '__dict__'):
                    config_cls.__dict__['arbitrary_types_allowed'] = True
                if hasattr(config_cls, 'arbitrary_types_allowed'):
                    setattr(config_cls, 'arbitrary_types_allowed', True)
        except Exception:
            pass
        
        try:
            # Check by name first (works even if BaseMessage isn't imported yet)
            if isinstance(type_, type):
                type_name = getattr(type_, '__name__', '')
                type_module = getattr(type_, '__module__', '')
                type_str = str(type_)
                # Check if it's BaseMessage by name and module
                if (type_name == 'BaseMessage' and 'langchain_core.messages.base' in type_module) or \
                   'BaseMessage' in type_str or 'langchain_core.messages.base.BaseMessage' in type_str or \
                   'messages.base.BaseMessage' in type_str:
                    # Return empty list to skip validation - this is the key!
                    return []
            
            # Also try to import and check BaseMessage properly
            try:
                from langchain_core.messages.base import BaseMessage
                
                # Check if type is BaseMessage or subclass
                if isinstance(type_, type):
                    try:
                        if issubclass(type_, BaseMessage):
                            # Enable arbitrary_types_allowed in config immediately
                            try:
                                if hasattr(model_config, '__dict__'):
                                    model_config.__dict__['arbitrary_types_allowed'] = True
                                if hasattr(model_config, 'arbitrary_types_allowed'):
                                    setattr(model_config, 'arbitrary_types_allowed', True)
                                if hasattr(model_config, '__class__'):
                                    config_cls = model_config.__class__
                                    if hasattr(config_cls, '__dict__'):
                                        config_cls.__dict__['arbitrary_types_allowed'] = True
                                    if hasattr(config_cls, 'arbitrary_types_allowed'):
                                        setattr(config_cls, 'arbitrary_types_allowed', True)
                            except Exception:
                                pass
                            # Return empty list to skip validation - this is the key!
                            return []
                    except TypeError:
                        # Not a class or not a subclass, continue
                        pass
            except (ImportError, AttributeError):
                # BaseMessage not available yet, continue
                pass
        except Exception:
            # If anything fails, continue to original validator
            pass
        
        # For all other types, use original validator finder
        if _original_find_validators is not None:
            try:
                return _original_find_validators(type_, model_config)
            except RuntimeError as e:
                # If error mentions BaseMessage, we should have caught it above
                # but if we didn't, try to handle it here
                error_str = str(e)
                if "BaseMessage" in error_str or "arbitrary_types_allowed" in error_str:
                    try:
                        from langchain_core.messages.base import BaseMessage
                        if isinstance(type_, type):
                            try:
                                if issubclass(type_, BaseMessage):
                                    # Force enable arbitrary_types_allowed
                                    try:
                                        if hasattr(model_config, '__dict__'):
                                            model_config.__dict__['arbitrary_types_allowed'] = True
                                        if hasattr(model_config, 'arbitrary_types_allowed'):
                                            setattr(model_config, 'arbitrary_types_allowed', True)
                                        if hasattr(model_config, '__class__'):
                                            config_cls = model_config.__class__
                                            if hasattr(config_cls, '__dict__'):
                                                config_cls.__dict__['arbitrary_types_allowed'] = True
                                            if hasattr(config_cls, 'arbitrary_types_allowed'):
                                                setattr(config_cls, 'arbitrary_types_allowed', True)
                                    except Exception:
                                        pass
                                    return []  # Return empty to skip validation
                            except TypeError:
                                pass
                    except (ImportError, AttributeError):
                        pass
                    # If we can't fix it, return empty list anyway to prevent error
                    return []
                # Re-raise if it's not a BaseMessage error
                raise
        else:
            # No original function, return empty (allow everything)
            return []
    
    # Patch the function
    pydantic_v1_validators.find_validators = patched_find_validators
    
    # Also patch at a lower level - catch RuntimeError during validator finding
    # This is a second layer of defense
    _original_find_validators_wrapped = patched_find_validators
    
    def double_patched_find_validators(type_, model_config):
        """Double-wrapped validator finder with additional error handling."""
        try:
            return _original_find_validators_wrapped(type_, model_config)
        except RuntimeError as e:
            error_str = str(e)
            if "BaseMessage" in error_str or "arbitrary_types_allowed" in error_str:
                # Force enable arbitrary_types_allowed and return empty validator list
                try:
                    # Try multiple ways to set arbitrary_types_allowed
                    if hasattr(model_config, '__dict__'):
                        model_config.__dict__['arbitrary_types_allowed'] = True
                    if hasattr(model_config, 'arbitrary_types_allowed'):
                        setattr(model_config, 'arbitrary_types_allowed', True)
                    # Also try to modify the class Config if available
                    if hasattr(model_config, '__class__'):
                        config_cls = model_config.__class__
                        if hasattr(config_cls, '__dict__'):
                            config_cls.__dict__['arbitrary_types_allowed'] = True
                        if hasattr(config_cls, 'arbitrary_types_allowed'):
                            setattr(config_cls, 'arbitrary_types_allowed', True)
                    # Return empty list to skip validation
                    return []
                except Exception:
                    # If we can't set it, return empty list anyway
                    return []
            # Re-raise if it's not a BaseMessage error
            raise
    
    pydantic_v1_validators.find_validators = double_patched_find_validators
except (ImportError, AttributeError) as e:
    # If we can't patch, that's okay - we'll handle it elsewhere
    pass

# Pre-import and patch langchain_community classes
try:
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        # Try to import and patch ChatMessageHistory before it's used
        try:
            from langchain_community.chat_message_histories.in_memory import ChatMessageHistory
            # Patch Pydantic v1 Config
            if hasattr(ChatMessageHistory, 'Config'):
                config = ChatMessageHistory.Config
                if not hasattr(config, 'arbitrary_types_allowed'):
                    config.arbitrary_types_allowed = True
                else:
                    ChatMessageHistory.Config.arbitrary_types_allowed = True
        except (ImportError, AttributeError, RuntimeError) as e:
            # Import may fail due to the BaseMessage issue, that's expected
            # We've patched the validator, so it should work on retry
            pass
except Exception:
    pass

