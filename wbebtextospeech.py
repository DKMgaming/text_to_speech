import pyttsx3
from pydub import AudioSegment
import tempfile
import os
import streamlit as st

def text_to_speech_vietnamese(text, rate):
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
        st.warning("Vietnamese voice not found. Using default voice.")
    
    engine.setProperty('rate', rate)
    
    # Tạo tệp WAV tạm thời
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_wav_file:
        temp_wav_path = temp_wav_file.name
    
    engine.save_to_file(text, temp_wav_path)
    engine.runAndWait()
    
    # Chuyển đổi sang MP3
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_mp3_file:
        temp_mp3_path = temp_mp3_file.name
    
    audio = AudioSegment.from_wav(temp_wav_path)
    audio.export(temp_mp3_path, format='mp3')
    
    os.remove(temp_wav_path)
    return temp_mp3_path

st.title("Text to Speech App - Vietnamese")

# Giao diện nhập liệu
text = st.text_area("Enter the text you want to convert to speech")
rate = st.number_input("Select the speaking rate", min_value=50, max_value=300, value=150)

if st.button("Convert to Speech"):
    if text.strip():
        output_mp3_path = text_to_speech_vietnamese(text, rate)
        
        # Phát âm thanh và cung cấp tùy chọn tải về
        audio_file = open(output_mp3_path, "rb")
        st.audio(audio_file, format="audio/mp3")
        st.download_button(
            label="Download MP3",
            data=audio_file,
            file_name="output.mp3",
            mime="audio/mp3"
        )
        
        # Xóa tệp tạm
        audio_file.close()
        os.remove(output_mp3_path)
    else:
        st.warning("Please enter some text to convert.")
