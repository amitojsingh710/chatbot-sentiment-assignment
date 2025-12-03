import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import threading
import time
import random
import os
from playaudio import playaudio
from gtts import gTTS 
from .chatbot import ChatBot
from .sentiment import SentimentAnalyzer
from .storage import ConversationStorage


class ChatUI:
    SENTIMENT_COLORS = {
        "Awesome": "#4caf50",
        "Good": "#8bc34a",
        "Neutral": "#9e9e9e",
        "Bad": "#ff9800",
        "Very Bad": "#f44336"
    }

    def __init__(self, root):
        self.root = root
        self.root.title("Premium Chatbot with Sentiment Analysis")
        self.root.geometry("800x700")
        self.root.configure(bg="#3B0000")

        # SPEECH RECOGNITION ONLY
        self.recognizer = sr.Recognizer()

        # Track conversation end
        self.conversation_ended = False
        self.last_bot_message = ""

        # Scrollable canvas
        self.canvas = tk.Canvas(root, bg="#f5f5f5")
        self.scrollbar = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#f5f5f5")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Input frame
        self.input_frame = tk.Frame(root, bg="#f5f5f5")
        self.input_frame.pack(fill=tk.X, padx=10, pady=5)

        self.entry = tk.Entry(self.input_frame, font=("Helvetica", 14), bd=1, relief=tk.FLAT)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5), pady=5)
        self.entry.bind("<Return>", self.send_message)

        # Mic Button (VOICE INPUT)
        self.mic_button = tk.Button(
            self.input_frame, text="🎤", font=("Helvetica", 14),
            command=self.voice_input
        )
        self.mic_button.pack(side=tk.RIGHT, padx=5)

        # Speak Button (VOICE OUTPUT)
        self.speak_button = tk.Button(
            self.input_frame, text="🔊", font=("Helvetica", 14),
            command=self.speak_last_bot_message
        )
        self.speak_button.pack(side=tk.RIGHT, padx=5)

        # Send button
        self.send_button = tk.Button(
            self.input_frame, text="Send", bg="#4caf50", fg="white",
            font=("Helvetica", 12, "bold"), command=self.send_message
        )
        self.send_button.pack(side=tk.RIGHT, pady=5)

        # End conversation
        self.end_button = tk.Button(
            root, text="End Conversation", bg="#2196f3", fg="white",
            font=("Helvetica", 12, "bold"), command=self.end_conversation
        )
        self.end_button.pack(side="bottom", pady=5)

        # Modules
        self.bot = ChatBot()
        self.analyzer = SentimentAnalyzer()
        self.storage = ConversationStorage()

    def speak_async(self, text):
        def speak_job():
            try:
                filename = f"tts_{int(time.time())}_{random.randint(1,9999)}.mp3"
                tts = gTTS(text=text, lang="en", tld="co.uk", slow=False)

                tts.save(filename)

                playaudio(filename)
                os.remove(filename)
            except Exception as e:
                print("TTS Error:", e)

        threading.Thread(target=speak_job, daemon=True).start()

    #####################################################################
    def display_message(self, role, message, sentiment=None):
        bubble_frame = tk.Frame(self.scrollable_frame, bg="#f5f5f5")
        bubble_frame.pack(fill="both", pady=5, padx=10)

        if role == "User":
            msg_label = tk.Label(
                bubble_frame, text=message, bg="#f7b8c6", fg="#000",
                wraplength=400, justify="left",
                font=("Helvetica", 12), padx=10, pady=5
            )
            msg_label.pack(anchor="e")

            if sentiment:
                sentiment_label = tk.Label(
                    bubble_frame, text=f"Sentiment: {sentiment}",
                    fg=self.SENTIMENT_COLORS.get(sentiment, "#000"),
                    bg="#f5f5f5", font=("Helvetica", 10, "italic")
                )
                sentiment_label.pack(anchor="e")
        else:
            msg_label = tk.Label(
                bubble_frame, text=message,
                bg="#e0e0e0", fg="#000",
                wraplength=400, justify="left",
                font=("Helvetica", 12), padx=10, pady=5
            )
            msg_label.pack(anchor="w")

        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1)

    #####################################################################
    def send_message(self, event=None):
        user_msg = self.entry.get()
        if not user_msg.strip():
            return

        sentiment = self.analyzer.analyze(user_msg)
        self.display_message("User", user_msg, sentiment)
        self.storage.add_message("User", user_msg, sentiment)

        bot_msg = self.bot.get_response(user_msg)
        self.last_bot_message = bot_msg

        self.display_message("Bot", bot_msg)
        self.storage.add_message("Bot", bot_msg)

        # SPEAK OUT LOUD — non-blocking
        self.speak_async(bot_msg)

        self.entry.delete(0, tk.END)

    #####################################################################
    def voice_input(self):
        try:
            with sr.Microphone() as source:
                self.display_message("Bot", "🎤 Listening...")
                audio = self.recognizer.listen(source)

            text = self.recognizer.recognize_google(audio)
            self.entry.delete(0, tk.END)
            self.entry.insert(0, text)
            self.send_message()

        except Exception:
            self.display_message("Bot", "Could not understand audio.")

    #####################################################################
    def speak_last_bot_message(self):
        if self.last_bot_message:
            self.speak_async(self.last_bot_message)

    #####################################################################
    def end_conversation(self):
        if self.conversation_ended:
            return

        self.conversation_ended = True
        self.storage.save()

        overall, score = self.compute_overall_sentiment()

        final_msg = (
            f"📊 FINAL REPORT\n"
            f"Sentiment: {overall}\n"
            f"Score: {score}"
        )

        self.display_message("Bot", final_msg)
        self.last_bot_message = final_msg

        self.speak_async(final_msg)

    #####################################################################
    def compute_overall_sentiment(self):
        user_scores = {"Awesome": 5, "Good": 3, "Neutral": 0, "Bad": -3, "Very Bad": -5}
        total = 0
        count = 0

        for msg in self.storage.messages:
            if msg["role"] == "User" and msg["sentiment"]:
                total += user_scores[msg["sentiment"]]
                count += 1

        score = total / count if count else 0

        if score >= 3:
            label = "very satisfied"
        elif score >= 1:
            label = "satisfied"
        elif score > -1:
            label = "average"
        elif score > -3:
            label = "unsatisfied"
        else:
            label = "very unsatisfied"

        return label, score

    #####################################################################
    def close_app(self):
        self.end_conversation()
        self.root.destroy()

    #####################################################################
    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.close_app)
        self.root.mainloop()
