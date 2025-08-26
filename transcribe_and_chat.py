import assemblyai as aai
import os

aai.settings.api_key = ""

def transcribe_audio(audio_file_path):
    if not os.path.exists(audio_file_path):
        raise FileNotFoundError(f"File not found: {audio_file_path}")
    transcriber = aai.Transcriber()
    transcript_obj = transcriber.transcribe(audio_file_path)
    if transcript_obj.status == "error" or not transcript_obj.text.strip():
        raise RuntimeError(f"Transcription failed: {transcript_obj.error}")
    return transcript_obj.text