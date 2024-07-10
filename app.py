from flask import Flask, render_template, request, send_file
import os
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key="api_key")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    # Check if file is present in the request
    if 'audio' not in request.files:
        return render_template('index.html', transcription="No audio file provided.")

    audio_file = request.files['audio']
    if audio_file.filename == '':
        return render_template('index.html', transcription="No audio file selected.")

    # Save the audio file temporarily
    audio_path = "temp_audio.mp3"
    audio_file.save(audio_path)

    # Read the audio file in binary mode
    with open(audio_path, "rb") as audio_file:
        # Call the OpenAI API to create a transcription
        transcript = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-1" 
        )
    
    # Extract the transcription text from the API response
    transcription = transcript.text
    
    # Delete the temporary audio file
    os.remove(audio_path)

    # Pass the transcription text to the download route
    return render_template('index.html', transcription=transcription)

@app.route('/download_transcription')
def download_transcription():
    # Get the transcription text from the query parameters
    transcription = request.args.get('transcription')
    
     # Create a temporary text file
    with open("transcription.txt", "w", encoding="utf-8") as text_file:
        text_file.write(transcription)
    
    # Send the file as an attachment
    return send_file("transcription.txt", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
