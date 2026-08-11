import os
from pathlib import Path
from dotenv import load_dotenv

# Project root:
# Smart-City-AI-Clean/
BASE_DIR = Path(__file__).resolve().parents[2]

# Load .env from project root
ENV_FILE = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_FILE)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")