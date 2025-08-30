import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY missing in .env")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

DATA_DIR = os.path.join(PROJECT_ROOT, "data")
UPLOAD_DIR = os.path.join(DATA_DIR, "uploads")
RESP_DIR = os.path.join(DATA_DIR, "responses")
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESP_DIR, exist_ok=True)

WHISPER_MODEL_NAME = "base"                 # change to "small" if needed
COQUI_MODEL_NAME = "tts_models/en/ljspeech/glow-tts"
TARGET_SR = 16000
TARGET_CHANNELS = 1
