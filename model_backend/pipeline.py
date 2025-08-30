import os
from typing import Dict
from .config import UPLOAD_DIR, RESP_DIR
from .services import ASRService, AIService, TTSService, ensure_wav_16k_mono, uid

class VoiceToVoiceModel:
    """
    File-in / file-out pipeline:
    - Input: path to audio file
    - Steps: normalize -> ASR -> LLM -> TTS
    - Output: dict with transcript, response_text, response_audio path
    """
    def __init__(self):
        self.asr = ASRService()
        self.ai = AIService()
        self.tts = TTSService(gpu=False)

    def process_file(self, input_audio_path: str) -> Dict[str, str]:
        job_id = uid()
        wav_path, _ = ensure_wav_16k_mono(input_audio_path)
        transcript = self.asr.transcribe(wav_path)
        response_text = self.ai.generate(transcript)
        out_path = os.path.join(RESP_DIR, f"{job_id}.wav")
        self.tts.synthesize_to_file(response_text, out_path)
        return {
            "id": job_id,
            "input_wav": wav_path,
            "transcript": transcript,
            "response_text": response_text,
            "response_audio": out_path
        }
