"""Custom exceptions for IntelliSupport"""

class IntelliSupportException(Exception):
    """Base exception for IntelliSupport"""
    pass

class EmbeddingException(IntelliSupportException):
    """Exception raised for embedding errors"""
    pass

class ChromaDBException(IntelliSupportException):
    """Exception raised for ChromaDB errors"""
    pass

class AgentException(IntelliSupportException):
    """Exception raised for agent errors"""
    pass

class LLMException(IntelliSupportException):
    """Exception raised for LLM errors"""
    pass

class ConfigException(IntelliSupportException):
    """Exception raised for configuration errors"""
    pass
