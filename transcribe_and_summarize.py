import assemblyai as aai
import openai
import os

aai.settings.api_key = ""
openai.api_key = ""


def summarize_audio_file(audio_file):
    if not os.path.exists(audio_file):
        raise FileNotFoundError(f"Audio file not found: {audio_file}")

    # Step 1: Transcribe
    config = aai.TranscriptionConfig(speech_model=aai.SpeechModel.best)
    transcript = aai.Transcriber(config=config).transcribe(audio_file)

    if transcript.status == "error" or not transcript.text.strip():
        raise RuntimeError(f"Transcription failed: {transcript.error}")

    text = transcript.text

    # Step 2: Chunk the transcript (by character count)
    def chunk_text(text, max_chunk_size=3000):
        chunks = []
        start = 0
        while start < len(text):
            end = start + max_chunk_size
            chunks.append(text[start:end])
            start = end
        return chunks

    chunks = chunk_text(text)

    # Step 3: Summarize each chunk
    client = openai.OpenAI(api_key=openai.api_key)
    summaries = []
    for i, chunk in enumerate(chunks):
        prompt = f"Summarize the following part of a podcast transcript clearly and concisely:\n\n{chunk}\n"
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes meeting transcripts. Please note when creating your response that you always mention meeting insted of transcript."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.5,
            )
            summary = response.choices[0].message.content.strip()
        except Exception as e:
            summary = f"Error summarizing chunk {i+1}: {e}"
        summaries.append(summary)

    # Step 4: Summarize all summaries
    final_prompt = "Summarize these summaries into a final concise summary:\n\n" + "\n\n".join(summaries)
    try:
        final_response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes meeting transcripts."},
                {"role": "user", "content": final_prompt}
            ],
            max_tokens=500,
            temperature=0.5,
        )
        final_summary = final_response.choices[0].message.content.strip()
    except Exception as e:
        final_summary = f"Error summarizing all summaries: {e}"

    print("\nFinal Summary:\n")
    print(final_summary)
    return final_summary, text  # Return both the summary and the full transcript