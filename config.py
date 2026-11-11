
import os

OLLAMA_HOST = os.getenv(
    "OLLAMA_HOST",
    "http://10.22.39.192:11434"
)

CHAT_MODEL = "qwen2.5vl:latest"

APP_TITLE = "AI Business Intelligence Analyst"

MAX_UPLOAD_SIZE_MB = 50
