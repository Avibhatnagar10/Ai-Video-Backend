# app/services/transcript_service.py

import whisper
import os
import uuid
import yt_dlp

AUDIO_DIR = os.path.join("downloads", "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

def download_audio(video_url: str) -> str:
    """Download audio from YouTube using yt-dlp."""
    unique_id = str(uuid.uuid4())
    output_path = os.path.join(AUDIO_DIR, f"{unique_id}.%(ext)s")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'noplaylist': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        downloaded_file = os.path.join(AUDIO_DIR, f"{info['id']}.mp3")
        if not os.path.exists(downloaded_file):
            # fallback to uuid file
            downloaded_file = os.path.join(AUDIO_DIR, f"{unique_id}.mp3")
        return downloaded_file

def get_transcript(video_url: str) -> dict:
    try:
        print(f"[TRANSCRIPT] Starting transcription for: {video_url}")
        audio_file = download_audio(video_url)
        print(f"[TRANSCRIPT] Audio downloaded to: {audio_file}")

        model = whisper.load_model("base")
        result = model.transcribe(audio_file)
        print("[TRANSCRIPT] Transcription successful.")

        os.remove(audio_file)
        print(f"[TRANSCRIPT] Cleaned up: {audio_file}")

        return {
            "text": result.get("text", ""),
            "segments": result.get("segments", []),
            "language": result.get("language", "unknown")
        }

    except Exception as e:
        print(f"[TRANSCRIPT] Error occurred: {e}")
        return {"error": str(e)}
