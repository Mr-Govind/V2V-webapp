import os
import re
import uuid
import subprocess
from typing import Tuple
from faster_whisper import WhisperModel
from TTS.api import TTS
import google.generativeai as genai

# Optional: ship an ffmpeg binary via imageio-ffmpeg if needed later
try:
    from imageio_ffmpeg import get_ffmpeg_exe
    FFMPEG_BIN = get_ffmpeg_exe()
except Exception:
    FFMPEG_BIN = "ffmpeg"  # fallback to system ffmpeg

from .config import (
    GEMINI_API_KEY, WHISPER_MODEL_NAME, COQUI_MODEL_NAME,
    TARGET_SR, TARGET_CHANNELS
)

genai.configure(api_key=GEMINI_API_KEY)

def clean_text(text: str) -> str:
    text = re.sub(r'[\*_#`]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

class ASRService:
    def __init__(self, model_name: str = WHISPER_MODEL_NAME):
        self.model = WhisperModel(model_name)

    def transcribe(self, wav_path: str) -> str:
        segments, _ = self.model.transcribe(wav_path)
        return " ".join(seg.text for seg in segments).strip()

class AIService:
    def __init__(self, model: str = "gemini-2.0-flash"):
        self.model = genai.GenerativeModel(model)

    def generate(self, prompt: str) -> str:
        resp = self.model.generate_content(prompt)
        return clean_text((getattr(resp, "text", "") or "").strip())

class TTSService:
    def __init__(self, model_name: str = COQUI_MODEL_NAME, gpu: bool = False):
        self.tts = TTS(model_name, gpu=gpu)

    def synthesize_to_file(self, text: str, out_path: str):
        self.tts.tts_to_file(text=text, file_path=out_path)

def convert_to_wav(src_path: str, dst_path: str, sr: int = TARGET_SR, ch: int = TARGET_CHANNELS):
    cmd = [FFMPEG_BIN, "-y", "-i", src_path, "-ar", str(sr), "-ac", str(ch), dst_path]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def ensure_wav_16k_mono(in_path: str) -> Tuple[str, bool]:
    ext = os.path.splitext(in_path)[1].lower()
    normalized = os.path.splitext(in_path)[0] + "_16k.wav"
    convert_to_wav(in_path, normalized)
    return normalized, True

def uid() -> str:
    return uuid.uuid4().hex
