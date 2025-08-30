# E.D.I.T.H Voice Assistant - Phase 4

<p align="center">A Voice and Text Conversational AI Assistant Web Application integrating speech recognition, large language models, and text-to-speech synthesis.</p>

---

## Table of Contents

- [About The Project](#about-the-project)  
- [Features](#features)  
- [Installation](#installation)  
- [Usage](#usage)  
- [Built With](#built-with)  
- [Contributing](#contributing)  
- [License](#license)  
- [Contact](#contact)  

---

## About The Project

This project delivers a fully functional web interface allowing users to interact with an AI assistant through voice commands and text input. It features real-time voice recording, transcription, response generation via AI models, and synthesized voice playback.

The architecture supports:

- Voice recording and ASR (Automatic Speech Recognition)  
- Text input processing  
- AI-powered language understanding and reply generation  
- Text-to-Speech (TTS) synthesis with Coqui TTS  
- Responsive and modern UI with clear user feedback  

---

## Features

- Record voice or type text queries  
- Real-time transcription display  
- Text replies and audio playback of responses  
- Clean, responsive web interface matching design mockups  
- Cross-browser support (Chrome, Firefox, Edge)  
- Robust error handling with status updates  

---

## Installation

### Prerequisites

- Python 3.8+  
- ffmpeg installed and in system PATH ([Download here](https://ffmpeg.org/download.html))  
- Git  

### Steps

git clone https://github.com/Mr-Govind/V2V-webapp.git
cd V2V-webapp
python -m venv project_env
project_env\Scripts\activate # Windows

OR
source project_env/bin/activate # macOS/Linux
pip install -r requirements.txt

text

---

## Usage

Start the Flask application:

python run.py

text

Open your browser and navigate to:

http://localhost:8000

text

Use the voice recording button or the text input bar to interact with the assistant.

---

## Built With

- Python 3  
- Flask  
- JavaScript (MediaRecorder API)  
- HTML / CSS  
- Coqui TTS  
- ffmpeg  
- Large Language Models (backend AI components)

---

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

---

## License

This project is licensed under the MIT License.

---

## Contact

**Mr Govind**  
- GitHub: [Mr-Govind](https://github.com/Mr-Govind)  
- Email: your-email@example.com  

---

<p align="center">Give a ⭐️ if this project helped you!</p>
