# Meeting Tools

A simple web app to make meetings easier to handle. Upload an MP3 file to get an AI-powered transcript, generate concise summaries, or ask questions directly about the meeting content.  
Built with **AssemblyAI** for transcription and **OpenAI** for summarization and Q&A.  

---

## Features
- 🎙️ **Transcription** – Convert meeting audio (MP3) into accurate text.
- 📝 **Summarization** – Generate clear, concise meeting summaries.
- 💬 **Chat with Meetings** – Ask questions directly about the meeting and get answers.
- 🌐 **Web UI** – Clean, minimal interface with tabs for Summarize and Chat modes.

---

## Project Structure
```
.
├── app.py                  # Backend server (Flask/FastAPI)
├── transcribe_and_chat.py  # Functions to transcribe audio and chat with it
├── transcribe_and_summarize.py # Functions to transcribe + summarize audio
├── summarize.py            # API route for summarization
├── index.html              # Frontend UI
└── README.md
```

---

## Requirements
- Python 3.8+
- AssemblyAI account + API key  
- OpenAI account + API key  

Install dependencies:
```bash
pip install flask assemblyai openai
```

---

## Setup
1. Clone this repo:
   ```bash
   git clone https://github.com/yourusername/meeting-tools.git
   cd meeting-tools
   ```

2. Add your API keys:
   - Open `transcribe_and_chat.py` and `transcribe_and_summarize.py`
   - Set:
     ```python
     aai.settings.api_key = "YOUR_ASSEMBLYAI_KEY"
     openai.api_key = "YOUR_OPENAI_KEY"
     ```

3. Run the backend server:
   ```bash
   python app.py
   ```

4. Open `index.html` in your browser.  
   Or, if the app serves HTML directly, navigate to:
   ```
   http://127.0.0.1:5000
   ```

---

## Usage
- **Summarize a Meeting**: Upload an `.mp3` file → Get a concise summary.  
- **Chat with a Meeting**: Upload `.mp3` and type a question → Get AI-generated answers.  

---

## Example
```bash
python transcribe_and_summarize.py my_meeting.mp3
```

Output:
```
Final Summary:
- Discussed project milestones
- Agreed on deadlines for Q2
- Assigned roles to team members
```

---

## Roadmap
- [ ] Add support for `.wav` and other audio formats  
- [ ] Export summaries to PDF/Markdown  
- [ ] Multi-language transcription  

---

## License
MIT License – free to use and modify.  
