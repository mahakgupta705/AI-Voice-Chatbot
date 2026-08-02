import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import speech_recognition as sr
from gtts import gTTS
import io

# Load API key securely
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="AI Voice Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 AI Voice Chatbot")
st.caption("Powered by Google Gemini API — Speak or Type")
st.markdown("**Created by Mahak Gupta**")





model = genai.GenerativeModel("gemini-flash-latest")

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])
    st.session_state.messages = []

# Show previous conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "audio" in message:
            st.audio(message["audio"], format="audio/mp3")

def speech_to_text(audio_bytes):
    recognizer = sr.Recognizer()
    with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
        audio_data = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio_data)
    except (sr.UnknownValueError, sr.RequestError):
        return None

def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp.read()

st.subheader("🎤 Speak your question")
audio_value = st.audio_input("Tap to record")

user_input = None

if audio_value:
    audio_bytes = audio_value.read()
    with st.spinner("Listening..."):
        recognized_text = speech_to_text(audio_bytes)
    if recognized_text:
        st.success(f"You said: {recognized_text}")
        user_input = recognized_text
    else:
        st.error("Sorry, couldn't understand. Try again or type below.")

typed_input = st.chat_input("...or type your message")
if typed_input:
    user_input = typed_input

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat.send_message(user_input)
            st.markdown(response.text)
            audio_response = text_to_speech(response.text)
            st.audio(audio_response, format="audio/mp3")

    st.session_state.messages.append({
        "role": "assistant",
        "content": response.text,
        "audio": audio_response
    })