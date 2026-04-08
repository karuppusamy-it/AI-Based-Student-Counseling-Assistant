import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB Configuration
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "student_counseling_db"

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Check required configuration
def check_config():
    if not OPENAI_API_KEY or OPENAI_API_KEY == "sk-...":
        print("Warning: OPENAI_API_KEY is not set or is using the default template value.")
    
    if not MONGO_URI:
        print("Warning: MONGO_URI is not set.")

# UI Settings
APP_NAME = "AI-Based Student Counseling Assistant"
DB_USERS_COLLECTION = "users"
DB_CHAT_COLLECTION = "chat_history"
