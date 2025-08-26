from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
import openai
import summarize
import transcribe_and_chat

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp3'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app = Flask(__name__)

openai.api_key = ""


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/summarize_mp3', methods=['POST'])
def summarize_mp3():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if not allowed_file(file.filename):
        return jsonify({'error': 'Only .mp3 files allowed'}), 400
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    try:
        summary = summarize.summarize_audio_file(filepath)
        return jsonify({'summary': summary})
    except Exception as e:
        return jsonify({'error': f"Summarization failed: {e}"}), 500

@app.route('/chat_with_mp3', methods=['POST'])
def chat_with_mp3():
    if 'file' not in request.files or 'question' not in request.form:
        return jsonify({'error': 'File and question required'}), 400
    file = request.files['file']
    question = request.form['question']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if not allowed_file(file.filename):
        return jsonify({'error': 'Only .mp3 files allowed'}), 400
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    try:
        transcript = transcribe_and_chat.transcribe_audio(filepath)
        prompt = (
            f"Meeting transcript:\n{transcript}\n\n"
            f"Based ONLY on the above transcript, answer the following question:\n{question}\n"
            f"If the answer is not in the transcript, say so."
        )
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for meetings. Answer only using the transcript."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=250,
            temperature=0.3,
        )
        answer = response.choices[0].message.content.strip()
        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'error': f"AI failed to answer: {e}"}), 500

@app.route('/', methods=['GET'])
def serve_frontend():
    return send_from_directory('.', 'index.html')

if __name__ == "__main__":
    app.run(debug=True)