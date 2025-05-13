import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# API Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyBxfzMOlpuR1QVBym_LeAayEqAfvn8ZcWs")
GOOGLE_CX = os.getenv("GOOGLE_CX", "94e638b8528184bdf")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")

GROQ_CHAT_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_SEARCH_URL = "https://api.groq.com/v1/search"

GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")  # Modèle utilisé dans la requête réussie
MEMORY_FILE = "chat_memory.json"
MAX_MESSAGES = 20  # Maximum messages to keep in history
LEAD_HISTORY_FILE = "lead_history.json"  # New file for lead history

# Configuration SMTP pour l'envoi d'emails
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "chedymiled@gmail.com")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "jdhq ltrb lnez rbyq")
DEFAULT_SENDER_NAME = os.getenv("DEFAULT_SENDER_NAME", "BID Consulting")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL", "houssemeddinekamkoum@gmail.com")