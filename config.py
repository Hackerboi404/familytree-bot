import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_ID = int(os.getenv("API_ID"))
    API_HASH = os.getenv("API_HASH")
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    
    # Database Path
    DATABASE_PATH = "database/family.db"
    
    # Log Channel (Optional: Put your channel ID here to log errors)
    LOG_CHANNEL = None
