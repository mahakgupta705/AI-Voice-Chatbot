import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import speech_recognition as sr
from gtts import gTTS
import io

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="AI Voice Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 AI Voice Chatbot")
st.caption("Powered by Google Gemini API — Speak or Type")
st.markdown("**Created by Mahak Gupta**")

# Faster, lightweight model
model = genai.GenerativeModel("gemini-flash-lite-latest")

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])
    st.session_state.messages = []

# Toggle: voice reply on/off (OFF by default = faster)
voice_reply = st.checkbox("🔊 Speak the AI's reply out loud", value=False)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "audio" in message and message["audio"]:
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
    try:
        tts = gTTS(text=text, lang='en')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp.read()
    except Exception:
        return None

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
        st.error("Couldn't understand. Try again or type below.")

typed_input = st.chat_input("...or type your message")
if typed_input:
    user_input = typed_input

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        reply_text = None
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.chat.send_message(
                    user_input,
                    request_options={"timeout": 15}
                )
                reply_text = response.text
                st.markdown(reply_text)
            except Exception as e:
                reply_text = "Sorry, I'm having trouble responding right now. Please try again in a moment."
                st.error(reply_text)

        audio_response = None
        if voice_reply and reply_text:
            with st.spinner("Generating voice..."):
                audio_response = text_to_speech(reply_text)
            if audio_response:
                st.audio(audio_response, format="audio/mp3")

    if reply_text:
        st.session_state.messages.append({
            "role": "assistant",
            "content": reply_text,
            "audio": audio_response
        })