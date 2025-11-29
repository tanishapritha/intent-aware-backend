import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SALESIQ_AUTH_TOKEN = os.getenv("SALESIQ_AUTH_TOKEN", "dummy_token")
    CLIQ_WEBHOOK_TOKEN = os.getenv("CLIQ_WEBHOOK_TOKEN", "dummy_token")
    CLIQ_CHANNEL_URL = os.getenv("CLIQ_CHANNEL_URL", "")
    CRM_API_KEY = os.getenv("CRM_API_KEY", "")
    
    # Model Configuration
    INTENT_MODEL_NAME = "typeform/distilbert-base-uncased-mnli"
    
    # Server Configuration
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))

settings = Config()
