import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'egemvp-secret-key-2026')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/egemvp.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OLLAMA_HOST = 'http://localhost:11434'
    OLLAMA_MODEL = 'qwen2.5:7b'