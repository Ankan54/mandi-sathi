import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Data.gov.in API Configuration
DATA_GOV_API_KEY = os.getenv("DATA_GOV_API_KEY", "")
DATA_GOV_RESOURCE_ID = "35985678-0d79-46b4-9ed6-6f13308a1d24"
DATA_GOV_API_URL = "https://api.data.gov.in/resource"

# Database Configuration
DATABASE_PATH = os.getenv("DATABASE_PATH", "mandi_saathi.db")

# Cache Configuration
CACHE_VALIDITY_HOURS = int(os.getenv("CACHE_VALIDITY_HOURS", "24"))

# Agent Configuration
AGENT_MODEL = "gpt-5.2"
AGENT_TEMPERATURE = 0.7

# Validation
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")
