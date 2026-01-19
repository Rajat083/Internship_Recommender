"""
Configuration settings for the Recommendation Service.
Centralizes all configuration parameters.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Model Configuration
MODEL_CONFIG = {
    'model_path': os.getenv('MODEL_PATH', 'Constants/trained_model.pkl'),
    'vectorizer_path': os.getenv('VECTORIZER_PATH', 'Constants/vectorizer.pkl'),
    'default_top_n': 5,
    'metric': 'cosine',
}

# Service Configuration
SERVICE_CONFIG = {
    'enable_caching': False,
    'cache_ttl': 3600,  # seconds
    'batch_size': 100,  # For batch processing
}

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_DATABASE"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "port": int(os.getenv("DB_PORT", 5432))
}

# Skill Processing Configuration
SKILL_CONFIG = {
    'normalize': True,
    'lowercase': True,
    'remove_duplicates': True,
    'min_skill_length': 2,
}

# Response Configuration
RESPONSE_CONFIG = {
    'include_explanation': False,
    'round_similarity_to': 4,  # decimal places
    'include_internship_details': True,
}

# Logging Configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
}


def get_model_config():
    """Get model configuration."""
    return MODEL_CONFIG.copy()


def get_service_config():
    """Get service configuration."""
    return SERVICE_CONFIG.copy()


def get_skill_config():
    """Get skill processing configuration."""
    return SKILL_CONFIG.copy()


def get_response_config():
    """Get response configuration."""
    return RESPONSE_CONFIG.copy()


def get_logging_config():
    """Get logging configuration."""
    return LOGGING_CONFIG.copy()
