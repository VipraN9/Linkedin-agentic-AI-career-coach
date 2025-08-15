import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")

# LLM Configuration
# Free models available on OpenRouter
FREE_LLM_MODEL = "mistralai/mistral-7b-instruct"  # Free tier model
BACKUP_LLM_MODEL = "meta-llama/llama-2-7b-chat"   # Alternative free model
PAID_LLM_MODEL = "openai/gpt-3.5-turbo"           # Paid model as backup

# Streamlit Configuration
STREAMLIT_SERVER_PORT = int(os.getenv("STREAMLIT_SERVER_PORT", 8501))
STREAMLIT_SERVER_ADDRESS = os.getenv("STREAMLIT_SERVER_ADDRESS", "0.0.0.0")

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
