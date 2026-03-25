import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "graph_db")
    
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    # Gemini - FIXED MODEL NAMES
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    # Use one of these valid model names:
    # - "gemini-1.5-flash" (fast, good for most tasks)
    # - "gemini-1.5-pro" (more capable, slower)
    # - "gemini-1.0-pro" (older version)
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash") 
    
    # App
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    DEBUG = ENVIRONMENT == "development"
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")
    
    # Graph
    MAX_NODES_VISIBLE = int(os.getenv("MAX_NODES_VISIBLE", "100"))
    DEFAULT_GRAPH_DEPTH = int(os.getenv("DEFAULT_GRAPH_DEPTH", "2"))