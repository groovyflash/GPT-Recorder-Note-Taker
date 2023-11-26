import pyaudio
import wave
import tkinter as tk
from tkinter import messagebox
import threading
import whisper
import time
import openai
from functools import partial
import ffmpeg
import yt_dlp
# import hvac
# import sys

openai.api_key = "" #your key here

# Settings
chunk = 2048
sample_format = pyaudio.paInt16
channels = 2
fs = 44100
filename = "output.wav"

# Function to convert mp4 to wav
def convert_to_wav(input_file, output_file):
    (
        ffmpeg
        .input(input_file)
        .output(output_file, acodec='pcm_s16le', y='-y')
        .run()
    )

# Function to download video and convert to wav
def getvideo(video, message):
    directory = "."
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
        'outtmpl': 'test.mp4'
    }
    # create a YoutubeDL object
    ydl = yt_dlp.YoutubeDL(ydl_opts)

    # download the video
    ydl.download([video])

    # convert the downloaded video to .wav
    input_file = directory + '/test.mp4'
    output_file = directory + '/output.wav'
    convert_to_wav(input_file, output_file)

p = pyaudio.PyAudio()

frames = []
stream = None
is_recording = False

def start_recording():
    global stream, is_recording
    if not is_recording:
        is_recording = True
        stream = p.open(format=sample_format,
                        channels=channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True)
        messagebox.showinfo("Recording", "Recording started.")
        threading.Thread(target=record_audio).start()

def record_audio():
    global frames
    while is_recording:
        data = stream.read(chunk, exception_on_overflow=False)
        frames.append(data)

def stop_recording():
    global is_recording, stream, frames
    if is_recording:
        is_recording = False
        stream.stop_stream()
        stream.close()

        if frames:  # Check if there are frames recorded
            wf = wave.open(filename, 'wb')
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(sample_format))
            wf.setframerate(fs)
            wf.writeframes(b''.join(frames))
            wf.close()
            frames = []  # Reset the frames list

            messagebox.showinfo("Recording", f"Recording stopped. File saved as {filename}")
            time.sleep(5)
        else:
            messagebox.showwarning("Recording", "No frames recorded.")

def transcribe_audio():
    time.sleep(5)
    # Load the whisper model
    model = whisper.load_model("tiny")
    options = whisper.DecodingOptions(language='en', fp16=False)
    
    # Transcribe the audio file
    audio_file = "output.wav"
    
    # Transcribe the audio
    result = model.transcribe(audio_file, fp16=False)
    
    # Extract the transcribed text from the result
    transcription = result["text"]
    with open("summary.txt", "w") as file:
        file.write(transcription)
    # Print the transcribed text
    print(transcription)

def get_bulleted_summary():
    time.sleep(5)
    try:
        # Read text from file
        with open("summary.txt", "r") as file:
            text = file.read()
        
        # Check the length of the text and divide it into chunks of 4000 characters each
        chunks = [text[i:i+4000] for i in range(0, len(text), 4000)]
        
        # Initialize a variable to store the complete summary
        complete_summary = ""
        
        # Loop through each chunk and make an API call
        for chunk in chunks:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a ChatGPT"
                    },
                    {"role": "user", "content": "in very detailed bullet points with specifics summarize what happened and any next steps " + chunk}
                ]
            )
            
            # Extract the summary from the response and append it to the complete summary
            summary = response['choices'][0]['message']['content']
            complete_summary += summary
        
        # Write the complete summary to a new file named 'bulletnotes.txt'
        with open("bulletnotes.txt", "w") as notes_file:
            notes_file.write(complete_summary)
        
        return "Summary written to bulletnotes.txt"

    except Exception as e:
        return f"An error occurred: {e}"

# Function to disable all buttons
def disable_buttons():
    start_button.config(state='disabled')
    stop_button.config(state='disabled')
    transcribe_button.config(state='disabled')
    summarize_button.config(state='disabled')

# Function to enable all buttons
def enable_buttons():
    start_button.config(state='normal')
    stop_button.config(state='normal')
    transcribe_button.config(state='normal')
    summarize_button.config(state='normal')

# Modify the command function to include disable/enable actions and delay
def command_with_delay(command, delay):
    disable_buttons()
    command()
    time.sleep(delay)
    enable_buttons()

# GUI
window = tk.Tk()
window.geometry("500x500")
window.title("Audio Recorder")

start_button = tk.Button(window, text="Start Recording", command=partial(start_recording))
start_button.pack(padx=20, pady=10)

stop_button = tk.Button(window, text="Stop Recording", command=partial(command_with_delay, stop_recording, 5))
stop_button.pack(padx=20, pady=10)

transcribe_button = tk.Button(window, text="Transcribe Audio", command=partial(command_with_delay, transcribe_audio, 5))
transcribe_button.pack(padx=20, pady=10)

summarize_button = tk.Button(window, text="Summarize Audio", command=partial(command_with_delay, get_bulleted_summary, 5))
summarize_button.pack(padx=20, pady=10)

# Add a new button for the getvideo function
# Note: You need to add your own video URL and message here
video_url = "https://www.youtube.com/watch?v=etw1sGCVvxE"
message = "your_message"
getvideo_button = tk.Button(window, text="Get Video", command=lambda: command_with_delay(partial(getvideo, video_url, message), 5))
getvideo_button.pack(padx=20, pady=10)
# getvideo_button = tk.Button(window, text="Get Video", command=partial(command_with_delay, getvideo, video_url, message, 5))
# getvideo_button.pack(padx=20, pady=10)

window.mainloop()

p.terminate()
