"""
Production configuration for Thesis Brainstorming Tool
"""
import os
from typing import List, Optional

class Settings:
    """Application settings"""
    
    # Application Info
    APP_NAME: str = "Thesis Brainstorming Tool"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "AI-powered thesis idea generator for academic research"
    
    # Environment
    ENVIRONMENT: str = "production" if os.getenv('VERCEL') else "development"
    DEBUG: bool = not bool(os.getenv('VERCEL'))
    
    # API Configuration
    GROQ_API_KEY: Optional[str] = os.getenv("GROQ_API_KEY")
    GROQ_BASE_URL: str = "https://api.groq.com/openai/v1"
    DEFAULT_MODEL: str = "llama-3.3-70b-versatile"
    
    # Rate Limiting
    MAX_REQUESTS_PER_MINUTE: int = int(os.getenv("MAX_REQUESTS_PER_MINUTE", "10"))
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "30"))
    
    # Security
    ALLOWED_ORIGINS: List[str] = (
        os.getenv("ALLOWED_ORIGINS", "").split(",") 
        if os.getenv("ALLOWED_ORIGINS") 
        else ["*"]
    )
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = int(os.getenv("PORT", 8001))
    
    # Validation Lists
    VALID_THESIS_TYPES: List[str] = [
        "argumentative", "analytical", "expository", "comparative"
    ]
    VALID_TONES: List[str] = [
        "academic", "persuasive", "neutral", "critical"
    ]
    
    # Limits
    MIN_FIELD_LENGTH: int = 2
    MAX_FIELD_LENGTH: int = 200
    MIN_IDEAS: int = 1
    MAX_IDEAS: int = 10
    
    # Caching
    STATIC_CACHE_MAX_AGE: int = 86400  # 24 hours
    
    @property
    def is_production(self) -> bool:
        """Check if running in production"""
        return self.ENVIRONMENT == "production"
    
    @property
    def api_configured(self) -> bool:
        """Check if API is configured"""
        return bool(self.GROQ_API_KEY)

# Global settings instance
settings = Settings() 