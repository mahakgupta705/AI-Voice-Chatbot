import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import speech_recognition as sr
from gtts import gTTS
import io

# -----------------------------
# API KEY
# -----------------------------
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY not found.")
    st.stop()

genai.configure(api_key=api_key)

# -----------------------------
# PAGE
# -----------------------------
st.set_page_config(
    page_title="AI Voice Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Voice Chatbot")
st.caption("Speak or Type")

# -----------------------------
# FAST GEMINI MODEL
# -----------------------------
model = genai.GenerativeModel(
    "gemini-2.5-flash-lite"
)

# -----------------------------
# CHAT SESSION
# -----------------------------
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# SHOW OLD MESSAGES
# -----------------------------
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message.get("audio"):
            st.audio(
                message["audio"],
                format="audio/mp3"
            )

# -----------------------------
# SPEECH TO TEXT
# -----------------------------
def speech_to_text(audio_bytes):

    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
            audio_data = recognizer.record(source)

        text = recognizer.recognize_google(
            audio_data,
            language="en-IN"
        )

        return text

    except:
        return None

# -----------------------------
# TEXT TO SPEECH
# -----------------------------
def text_to_speech(text):

    try:

        tts = gTTS(
            text=text,
            lang="en"
        )

        audio = io.BytesIO()

        tts.write_to_fp(audio)

        audio.seek(0)

        return audio.read()

    except:
        return None

# -----------------------------
# VOICE INPUT
# -----------------------------
st.subheader("🎤 Speak your question")

audio_value = st.audio_input(
    "Tap to record"
)

user_input = None

if audio_value:

    audio_bytes = audio_value.read()

    with st.spinner("Listening..."):

        recognized_text = speech_to_text(
            audio_bytes
        )

    if recognized_text:

        st.success(
            f"You said: {recognized_text}"
        )

        user_input = recognized_text

    else:

        st.error(
            "Couldn't understand. Please try again."
        )

# -----------------------------
# TEXT INPUT
# -----------------------------
typed_input = st.chat_input(
    "Or type your message..."
)

if typed_input:
    user_input = typed_input

# -----------------------------
# GEMINI RESPONSE
# -----------------------------
if user_input:

    # User message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # AI response
    with st.chat_message("assistant"):

        response_box = st.empty()

        full_response = ""

        try:

            response = (
                st.session_state.chat
                .send_message(
                    user_input,
                    stream=True
                )
            )

            # Show text immediately as chunks arrive
            for chunk in response:

                if chunk.text:

                    full_response += chunk.text

                    response_box.markdown(
                        full_response
                    )

            # Voice AFTER text is complete
            audio_response = text_to_speech(
                full_response
            )

            if audio_response:

                st.audio(
                    audio_response,
                    format="audio/mp3"
                )

        except Exception as e:

            full_response = f"Error: {e}"

            response_box.error(
                full_response
            )

            audio_response = None

    # Save response
    st.session_state.messages.append({
        "role": "assistant",
        "content": full_response,
        "audio": audio_response
    })