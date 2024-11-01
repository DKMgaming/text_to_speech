from gtts import gTTS
import tempfile
import streamlit as st
import os

def text_to_speech_vietnamese(text, lang='vi'):
    tts = gTTS(text=text, lang=lang, slow=False)
    
    # Tạo tệp MP3 tạm thời
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_mp3_file:
        temp_mp3_path = temp_mp3_file.name
    tts.save(temp_mp3_path)
    
    return temp_mp3_path

st.title("Text to Speech App - Vietnamese")

# Giao diện nhập liệu
text = st.text_area("Enter the text you want to convert to speech")
rate = st.number_input("Select the speaking rate (not applicable with gTTS)", min_value=50, max_value=300, value=150)

if st.button("Convert to Speech"):
    if text.strip():
        output_mp3_path = text_to_speech_vietnamese(text)
        
        # Phát âm thanh và cung cấp tùy chọn tải về
        audio_file = open(output_mp3_path, "rb")
        st.audio(audio_file, format="audio/mp3")
        st.download_button(
            label="Download MP3",
            data=audio_file,
            file_name="output.mp3",
            mime="audio/mp3"
        )
        
        # Đóng và xóa tệp tạm
        audio_file.close()
        os.remove(output_mp3_path)
    else:
        st.warning("Please enter some text to convert.")
