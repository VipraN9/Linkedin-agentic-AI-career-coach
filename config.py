import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables for local development
load_dotenv()

# Function to get secrets from Streamlit Cloud or environment variables
def get_secret(key, default=None):
    """Get secret from Streamlit Cloud or environment variable"""
    try:
        # Try to get from Streamlit secrets first (for Streamlit Cloud)
        if hasattr(st, 'secrets') and st.secrets:
            return st.secrets.get(key, default)
    except:
        pass
    
    # Fallback to environment variables (for local development)
    return os.getenv(key, default)

# API Keys
OPENROUTER_API_KEY = get_secret("OPENROUTER_API_KEY")
APIFY_API_TOKEN = get_secret("APIFY_API_TOKEN")

# LLM Configuration
# Free models available on OpenRouter
FREE_LLM_MODEL = "mistralai/mistral-7b-instruct"  # Free tier model
BACKUP_LLM_MODEL = "meta-llama/llama-2-7b-chat"   # Alternative free model
PAID_LLM_MODEL = "openai/gpt-3.5-turbo"           # Paid model as backup

# Streamlit Configuration
STREAMLIT_SERVER_PORT = int(get_secret("STREAMLIT_SERVER_PORT", 8501))
STREAMLIT_SERVER_ADDRESS = get_secret("STREAMLIT_SERVER_ADDRESS", "0.0.0.0")

# App Configuration
APP_NAME = "LinkedIn Profile Optimizer"
APP_VERSION = "1.0.0"

# Memory Configuration
MEMORY_TTL = 3600  # 1 hour in seconds
MAX_MEMORY_SIZE = 1000  # Maximum number of messages to store

# Chat Configuration
MAX_TOKENS = 4000
TEMPERATURE = 0.7

# Job Analysis Configuration
JOB_MATCH_THRESHOLD = 0.6
