Premium Chatbot with Sentiment Analysis

1) Features:
   -> Interactive Chat UI built with Tkinter

   Tier 1:
   -> Overall conversation summary at the end of each session with a sentiment score

   -> JSON-based conversation storage for full chat history

   Tier 2:
   -> Statement-level sentiment analysis: Classifies user messages as Awesome / Good / Neutral / Bad / Very Bad

   Additional Features:
   -> Voice input & output: Speak to the bot and hear responses

   -> Modular Python code for easy maintenance and extension

   -> Unit tests included for core modules

2) How to Run:

Activate virtual environment

   # Windows
   .\venv\Scripts\activate
   # Linux/macOS
   source venv/bin/activate


Run the app

   python -m scripts.run_app


Chat with the bot in the GUI

   End the conversation by clicking "End Conversation" to see the overall sentiment report

3) 🛠 Technologies Used

   -> Python 3.12+

   -> Tkinter – GUI

   -> NLTK (VADER) – Sentiment analysis

   -> gTTS  – Text-to-speech output

   -> speech_recognition – Voice input from microphone

   -> Markovify – Fallback response generation

   -> JSON – Conversation storage

   -> Pytest – Unit testing


4) Unit Testing

To run tests, use pytest in your project root:

   pytest

Tests cover core modules like chatbot.py, sentiment.py, and storage.py.