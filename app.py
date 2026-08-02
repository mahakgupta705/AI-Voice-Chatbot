import io
import os

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types
import speech_recognition as sr
from gtts import gTTS


# --------------------------------------------------
# PAGE SETTINGS
# --------------------------------------------------

st.set_page_config(
    page_title="AI Voice Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Voice Chatbot")
st.caption("Powered by Gemini • Speak or Type")


# --------------------------------------------------
# API KEY
# --------------------------------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

# Streamlit Cloud Secrets
if not api_key:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        api_key = None

if not api_key:
    st.error("GEMINI_API_KEY not found.")
    st.stop()


# --------------------------------------------------
# GEMINI CLIENT
# --------------------------------------------------

client = genai.Client(api_key=api_key)

MODEL = "gemini-2.5-flash"


# --------------------------------------------------
# CHAT SESSION
# --------------------------------------------------

if "chat" not in st.session_state:

    st.session_state.chat = client.chats.create(
        model=MODEL,
        config=types.GenerateContentConfig(
            temperature=0.4,
            max_output_tokens=500,
            thinking_config=types.ThinkingConfig(
                thinking_budget=0
            )
        )
    )

if "messages" not in st.session_state:
    st.session_state.messages = []


# --------------------------------------------------
# TEXT TO SPEECH
# --------------------------------------------------

def text_to_speech(text, language="en"):

    audio_file = io.BytesIO()

    tts = gTTS(
        text=text,
        lang=language,
        slow=False
    )

    tts.write_to_fp(audio_file)

    audio_file.seek(0)

    return audio_file.read()


# --------------------------------------------------
# SPEECH TO TEXT
# --------------------------------------------------

def speech_to_text(audio_bytes):

    recognizer = sr.Recognizer()

    try:

        with sr.AudioFile(io.BytesIO(audio_bytes)) as source:

            audio_data = recognizer.record(source)

        text = recognizer.recognize_google(audio_data)

        return text

    except sr.UnknownValueError:

        return None

    except sr.RequestError:

        return None

    except Exception:

        return None


# --------------------------------------------------
# DISPLAY OLD MESSAGES
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message.get("audio"):

            st.audio(
                message["audio"],
                format="audio/mp3"
            )


# --------------------------------------------------
# VOICE INPUT
# --------------------------------------------------

st.subheader("🎤 Speak your question")

audio_value = st.audio_input(
    "Tap to record",
    sample_rate=16000
)

voice_text = None

if audio_value:

    audio_bytes = audio_value.read()

    with st.spinner("Converting voice to text..."):

        voice_text = speech_to_text(audio_bytes)

    if voice_text:

        st.info(f"You said: {voice_text}")

    else:

        st.error(
            "Sorry, I couldn't understand your voice. "
            "Please try again or type your question."
        )


# --------------------------------------------------
# TEXT INPUT
# --------------------------------------------------

typed_text = st.chat_input(
    "Or type your message..."
)


# Voice has priority if available
user_input = voice_text if voice_text else typed_text


# --------------------------------------------------
# GENERATE RESPONSE
# --------------------------------------------------

if user_input:

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)


    with st.chat_message("assistant"):

        response_placeholder = st.empty()

        full_response = ""

        try:

            # STREAM RESPONSE
            response_stream = (
                st.session_state.chat.send_message_stream(
                    user_input
                )
            )

            for chunk in response_stream:

                if chunk.text:

                    full_response += chunk.text

                    response_placeholder.markdown(
                        full_response + "▌"
                    )

            # Remove cursor
            response_placeholder.markdown(
                full_response
            )


            # ------------------------------------------
            # VOICE RESPONSE
            # ------------------------------------------

            if full_response:

                with st.spinner("Preparing voice..."):

                    audio_response = text_to_speech(
                        full_response,
                        language="en"
                    )

                st.audio(
                    audio_response,
                    format="audio/mp3"
                )

            else:

                audio_response = None


        except Exception as e:

            full_response = f"Error: {e}"

            response_placeholder.error(
                full_response
            )

            audio_response = None


    # Save assistant message

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": full_response,
            "audio": audio_response
        }
    )