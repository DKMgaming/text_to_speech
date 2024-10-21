from flask import Flask, render_template, request, send_file
import pyttsx3
from pydub import AudioSegment
import tempfile
import os

app = Flask(__name__)

def text_to_speech_vietnamese(text, filename, rate):
    engine = pyttsx3.init()

    voices = engine.getProperty('voices')
    
    vietnamese_voice_id = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\MSTTS_V110_viVN_An"
    voice_found = False
    for voice in voices:
        if voice.id == vietnamese_voice_id:
            engine.setProperty('voice', voice.id)
            voice_found = True
            break
    
    if not voice_found:
        print("Vietnamese voice not found. Using default voice.")
    
    engine.setProperty('rate', rate)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_wav_file:
        temp_wav_path = temp_wav_file.name
    
    engine.save_to_file(text, temp_wav_path)
    engine.runAndWait()
    
    audio = AudioSegment.from_wav(temp_wav_path)
    audio.export(filename, format='mp3')
    
    os.remove(temp_wav_path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    text = request.form['text']
    rate = int(request.form['rate'])
    
    # Tạo tệp âm thanh và trả về cho người dùng
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_mp3_file:
        temp_mp3_path = temp_mp3_file.name
    text_to_speech_vietnamese(text, temp_mp3_path, rate)
    
    return send_file(temp_mp3_path, as_attachment=True, download_name="output.mp3")

if __name__ == '__main__':
    app.run(debug=True)
