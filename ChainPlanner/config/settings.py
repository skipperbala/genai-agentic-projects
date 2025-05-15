# config/settings.py

import os
from dotenv import load_dotenv
load_dotenv()
MODEL_NAME = os.getenv("MODEL_NAME", "llama3")
MEMORY_PATH = os.getenv("MEMORY_PATH", "data/memory_index")
APP_MODE = os.getenv("APP_MODE", "streamlit")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
CALENDAR_API_KEY = os.getenv("CALENDAR_API_KEY", "")
