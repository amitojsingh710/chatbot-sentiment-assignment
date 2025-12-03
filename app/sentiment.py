from nltk.sentiment import SentimentIntensityAnalyzer

class SentimentAnalyzer:
    """Analyzes user messages and returns sentiment labels"""
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()

    def analyze(self, text: str) -> str:
        score = self.sia.polarity_scores(text)['compound']
        if score >= 0.6:
            return "Awesome"
        elif score >= 0.2:
            return "Good"
        elif score > -0.2:
            return "Neutral"
        elif score > -0.6:
            return "Bad"
        else:
            return "Very Bad"
