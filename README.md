# GPT-Recorder-Note-Taker

# Audio Recorder and Summarizer

## Description
This application provides a simple interface for recording audio, downloading and processing videos from YouTube, transcribing audio content, and summarizing the transcribed text using OpenAI's GPT models. It's designed exclusively for macOS users.

## Features
- Record audio directly through the application.
- Download videos from YouTube and convert them to audio format.
- Transcribe audio content using the Whisper model.
- Summarize transcribed text with the help of OpenAI's GPT models.

## Prerequisites
- macOS operating system.
- BlackHole 2Ch installed for audio capture.
- Python 3.x
- Required Python packages: `pyaudio`, `wave`, `tkinter`, `threading`, `whisper`, `time`, `openai`, `ffmpeg`, `yt-dlp`, `functools`.

## Installation
1. Clone the repository or download the source code.
2. Install BlackHole 2Ch for audio routing (necessary for capturing audio on macOS).
3. Install required Python packages:
   ```bash
   pip install pyaudio wave tkinter threading whisper time openai ffmpeg yt-dlp functools
## Useage
Run the script to open the GUI: python script_name.py.
Use the buttons in the GUI to:
Start/Stop audio recording.
Download and process YouTube videos.
Transcribe audio content.
Summarize the transcribed text.
The application will save the audio, transcription, and summaries in the same directory.

## Important Notes
Ensure you're not running too many applications simultaneously as this script uses multiple threads which might stress lower-end systems.
Only use this application on a macOS system with BlackHole 2Ch installed.
Make sure to handle your OpenAI API key securely and avoid exposing it in shared or public environments.
