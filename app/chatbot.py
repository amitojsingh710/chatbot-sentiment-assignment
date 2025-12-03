import random
import markovify 
import os
import speech_recognition as sr 
from gtts import gTTS 
import tempfile

from playaudio import playaudio

class ChatBot:
    def __init__(self):
        # Keyword-based responses
        self.keyword_responses = {
        # Greetings
        "hello": ["Hi there! How can I help you today?", "Hello! What's up?"],
        "hi": ["Hello! How can I help you?", "Hi! Nice to meet you."],
        "hey": ["Hey! How can I help?", "Hi there! What can I do for you?"],
        "greetings": ["Greetings! How may I assist?", "Hello! How can I support you today?"],

        # Positive emotions & experiences
        "happy": ["I'm glad you're feeling good!", "That's wonderful to hear!"],
        "good": ["I'm glad things are going well!", "Happy to hear that!"],
        "great": ["That's great to hear!", "Awesome—I'm glad things are going well."],
        "amazing": ["That's amazing!", "Happy to hear such great news!"],
        "excellent": ["Excellent! Let me know if you need anything else.", "Glad to hear that!"],
        "awesome": ["Awesome! I'm here if you need more help.", "Great news!"],
        "positive": ["Glad you're feeling positive!", "That's great to hear!"],
        "fine": ["I'm glad you're doing fine!", "Good to hear!"],

        # Appreciation
        "thanks": ["You're welcome!", "Anytime!"],
        "thank you": ["You're welcome! Happy to help.", "No problem at all!"],
        "thx": ["You're welcome!", "Glad to help!"],

        # Neutral/help-seeking words
        "help": ["Sure! How can I help you?", "I'm here—what do you need help with?"],
        "support": ["I'm here to support you. Tell me what's going on.", "How can I support you today?"],
        "question": ["Go ahead—what's your question?", "Ask away! I'm here to help."],
        "info": ["I can provide information. What would you like to know?", "Sure—what info do you need?"],
        
        # Negative emotions & experiences
        "problem": ["I'm sorry to hear that. Can you tell me more?", "Oh no! What happened?"],
        "issue": ["Let's try to solve it together.", "Can you explain the issue?"],
        "bad": ["I'm sorry you're feeling that way.", "Let's see how I can help make things better."],
        "sad": ["I'm sorry you're feeling sad. I'm here for you.", "That sounds tough. How can I help?"],
        "upset": ["I'm sorry you're upset. Want to talk about it?", "I'm here—tell me what's bothering you."],
        "angry": ["I understand you're feeling angry. Let’s try to fix this together.", "I'm sorry you're upset—how can I help?"],
        "frustrated": ["I'm sorry you're frustrated. Let’s take it step by step.", "I understand—that can be frustrating. I'm here to help."],
        "confused": ["I can clarify things. What’s confusing you?", "Let me explain it more clearly."],
        "annoyed": ["I'm sorry you're annoyed. Let’s sort this out.", "That sounds frustrating—how can I help?"],
        "disappointing": ["I’m sorry it felt disappointing. Let me help fix it.", "Thanks for sharing—let’s improve things."],
        "unhappy": ["I’m sorry you’re unhappy. How can I help?", "Let me know what went wrong so I can assist."],
        "worried": ["I understand you're worried. Let's talk about it.", "I'm here—what concerns you?"],
        "stressed": ["I'm sorry you're stressed. How can I help make things easier?", "Let’s take it one step at a time."],

        # Negative service-related words
        "slow": ["Sorry for the slow experience—I'll help speed things up.", "I apologize for the delay. Let me assist."],
        "unhelpful": ["I'm sorry that wasn't helpful. Let me assist now.", "Let’s try again—I’m here to help."],
        "rude": ["I'm sorry you had that experience. That shouldn't happen.", "Thanks for telling me—I can look into it."],
        "unresponsive": ["Sorry for not responding sooner. I'm here now.", "I apologize for the delay—let’s continue."],
        "inconvenient": ["Sorry for the inconvenience. I’ll help sort it out.", "Let me try to make things easier for you."],
        "difficult": ["Sorry it felt difficult. I can guide you.", "Let’s work through this together."],
        "confusing": ["I can clarify that! Tell me what part is unclear.", "Let me explain it more simply."],

        # Neutral conversational context
        "okay": ["Alright! How else can I help?", "Okay—let me know what you need."],
        "ok": ["Okay! I'm here if you need anything.", "Got it! What next?"],
        "sure": ["Great! What do you need help with?", "Alright! How can I assist?"],
        "maybe": ["Take your time—I'm here if you need anything.", "Let me know whenever you're ready."],

        # Farewell
        "bye": ["Goodbye! Have a great day!", "See you later!"],
        "goodbye": ["Take care! See you next time.", "Goodbye! I'm here whenever you need me."],
        "see you": ["See you soon!", "Whenever you need me, I’ll be here."],
        }


        # Load Markov corpus
        corpus_path = os.path.join(os.path.dirname(__file__), "data", "corpus.txt")
        if os.path.exists(corpus_path):
            with open(corpus_path, "r", encoding="utf-8") as f:
                text = f.read()
            self.markov_model = markovify.Text(text)
        else:
            self.markov_model = None

        # For voice
        self.recognizer = sr.Recognizer()

    # ---------------------------------------------------
    # 🔊 Text → Speech (Bot speaks)
    # ---------------------------------------------------
    def speak(self, text):
        try:
            tts = gTTS(text=text, lang="en")
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tts.save(tmp.name)
            
            playaudio(tmp)
        except Exception as e:
            print("TTS Error:", e)

    # ---------------------------------------------------
    # 🎤 Speech → Text (Mic input)
    # ---------------------------------------------------
    def listen(self, timeout=5, phrase_time_limit=10):
        """Return text spoken through the mic."""
        try:
            with sr.Microphone() as source:
                print("Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.4)
                audio = sr.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            text = self.recognizer.recognize_google(audio)
            print("Recognized:", text)
            return text

        except Exception as e:
            print("Mic Error:", e)
            return None

    # ---------------------------------------------------
    # 🤖 Text Response Logic
    # ---------------------------------------------------
    def get_response(self, user_input):
        if not user_input:
            return "Sorry, I couldn't hear you clearly."

        user_input = user_input.lower()

        # Keyword logic
        for keyword, responses in self.keyword_responses.items():
            if keyword in user_input:
                return random.choice(responses)

        # Markov fallback
        if self.markov_model:
            sentence = self.markov_model.make_sentence(tries=5)
            if sentence:
                return sentence

        # Final fallback
        return random.choice(["Interesting...", "Tell me more!", "I see.", "Could you elaborate?"])
