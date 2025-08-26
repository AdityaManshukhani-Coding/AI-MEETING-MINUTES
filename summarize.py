import assemblyai as aai
import openai
import os

aai.settings.api_key = ""
openai.api_key = ""

def summarize_audio_file(audio_file):
    if not os.path.exists(audio_file):
        raise FileNotFoundError(f"Audio file not found: {audio_file}")
    transcript_obj = aai.Transcriber().transcribe(audio_file)
    if transcript_obj.status == "error" or not transcript_obj.text.strip():
        raise RuntimeError(f"Transcription failed: {transcript_obj.error}")
    text = transcript_obj.text

    prompt = f"Summarize the following meeting transcript:\n{text}\n"
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes meetings. Please note when creating your response that you always mention meeting insted of transcript."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        temperature=0.5,
    )
    summary = response.choices[0].message.content.strip()
    return summary