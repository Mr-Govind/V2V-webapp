from flask import Blueprint, request, jsonify, current_app, send_from_directory, url_for
import os
import uuid

# Import the pipeline class from your model package
from model_backend import VoiceToVoiceModel

api_bp = Blueprint("api", __name__)

# Initialize the heavy pipeline once at import time
v2v = VoiceToVoiceModel()
# v2v = None
# def get_pipeline():
#     global v2v
#     if v2v is None:
#         v2v = VoiceToVoiceModel()
#     return v2v


def _uid() -> str:
    return uuid.uuid4().hex

@api_bp.get("/health")
def health():
    return jsonify({"status": "ok"})

@api_bp.post("/process")
def process_audio():
    """
    Accepts multipart/form-data with file field 'audio'.
    Saves upload -> normalizes -> ASR -> Gemini -> TTS.
    Returns JSON with transcript, response_text, and audio_url.
    """
    f = request.files.get("audio")
    if not f:
        return jsonify({"error": "No file uploaded. Use form-data field 'audio'."}), 400

    # Paths
    upload_dir = current_app.config["UPLOAD_DIR"]
    resp_dir = current_app.config["RESP_DIR"]
    os.makedirs(upload_dir, exist_ok=True)
    os.makedirs(resp_dir, exist_ok=True)

    # Save uploaded file with unique id and original extension
    root, ext = os.path.splitext(f.filename or "")
    ext = (ext or ".bin").lower()
    in_path = os.path.join(upload_dir, f"{_uid()}{ext}")
    f.save(in_path)

    try:
        result = v2v.process_file(in_path)
    except Exception as e:
        return jsonify({"error": f"Processing failed: {e}"}), 500

    # Build a public URL for the synthesized audio
    audio_name = os.path.basename(result["response_audio"])
    audio_url = url_for("api.serve_audio", name=audio_name, _external=False)

    return jsonify({
        "id": result["id"],
        "transcript": result["transcript"],
        "response_text": result["response_text"],
        "audio_url": audio_url
    })

@api_bp.post("/text")
def process_text():
    """
    Accepts application/json: { "text": "..." }
    Runs LLM -> TTS (no ASR) and returns JSON with response_text and audio_url.
    """
    data = request.get_json(silent=True) or {}
    user_text = (data.get("text") or "").strip()
    if not user_text:
        return jsonify({"error": "Missing 'text' in JSON body"}), 400

    try:
        # Generate reply
        reply = v2v.ai.generate(user_text)

        # Synthesize speech
        resp_dir = current_app.config["RESP_DIR"]
        os.makedirs(resp_dir, exist_ok=True)
        name = f"{_uid()}.wav"
        out_path = os.path.join(resp_dir, name)
        v2v.tts.synthesize_to_file(reply, out_path)

        audio_url = url_for("api.serve_audio", name=name, _external=False)
        return jsonify({
            "response_text": reply,
            "audio_url": audio_url
        })
    except Exception as e:
        return jsonify({"error": f"Text processing failed: {e}"}), 500

@api_bp.get("/audio/<path:name>")
def serve_audio(name: str):
    """
    Serves synthesized audio files from data/responses.
    """
    resp_dir = current_app.config["RESP_DIR"]
    return send_from_directory(resp_dir, name, mimetype="audio/wav")
# Note: In production, consider using a more robust method to serve static files.