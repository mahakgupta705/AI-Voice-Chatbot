# AI Voice Chatbot 🎙️🤖

An intelligent chatbot built with Python and Streamlit, powered by Google's **Gemini API**. This chatbot supports both **text and voice conversations** — speak your question and hear the AI respond back in a natural voice.

## ✨ Features

- 💬 Real-time AI-powered responses using Google's Gemini model
- 🎤 **Voice input** — speak your questions using the microphone
- 🔊 **Voice output** — AI replies are read aloud automatically
- ⌨️ Text input also supported for flexibility
- 🧠 Maintains conversation history/context during a session
- 🎨 Clean, modern web interface built with Streamlit
- 🔒 Secure API key handling using environment variables

## 🚀 Live Demo

Try it out here: [AI Voice Chatbot](https://ai-voice-chatbot-tsxqlxzdw8jqsrcna3kcty.streamlit.app/)

## 🛠️ Tech Stack

- **Python 3**
- **Streamlit** — for the web interface
- **Google Generative AI (Gemini API)** — for AI responses
- **SpeechRecognition** — for converting voice to text
- **gTTS (Google Text-to-Speech)** — for converting text to voice
- **python-dotenv** — for secure environment variable management

## 📋 Prerequisites

- Python 3.8 or higher
- A Google AI Studio account and API key ([Get one here](https://aistudio.google.com/apikey))

## 🚀 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/mahakgupta705/AI-Voice-Chatbot.git
   cd AI-Voice-Chatbot
   ```

2. **Install the required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**

   Create a `.env` file in the project's root directory and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

   ⚠️ **Never share your `.env` file or commit it to GitHub.**

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

   This will automatically open the chatbot in your browser.

## 💬 Usage

- Type your message in the chat box, **or**
- Tap the microphone button and speak your question
- The AI will respond in both text and audio

## 📁 Project Structure

```
AI-Voice-Chatbot/
│
├── app.py                # Main Streamlit application
├── requirements.txt      # Python dependencies
├── .env                   # API key (not tracked by Git)
├── .gitignore             # Files/folders excluded from Git
└── README.md              # Project documentation
```

## 🔒 Security Note

This project uses environment variables to keep the API key secure and out of the source code. When deploying, add your API key via the hosting platform's secrets manager instead of committing it to the repository.

## 🎯 Future Improvements

- [ ] Support for multiple languages in voice input/output
- [ ] Continuous, hands-free conversation mode
- [ ] Save and load past conversation history
- [ ] Custom voice selection for responses

## 📄 License

This project is open source and available for educational purposes.

## 🙋‍♀️ Author

**Mahak Gupta**

---

⭐ If you found this project helpful, consider giving it a star on GitHub!
