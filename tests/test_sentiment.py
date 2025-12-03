from app.sentiment import SentimentAnalyzer

def test_edge_sentiments():
    analyzer = SentimentAnalyzer()
    
    # Extreme positive
    assert analyzer.analyze("I absolutely love this!") in ["Awesome", "Good"]
    
    # Slight positive
    assert analyzer.analyze("This is okay") in ["Good", "Neutral"]
    
    # Neutral / mild positive
    assert analyzer.analyze("It's fine") in ["Good", "Neutral"]
    
    # Slight negative
    assert analyzer.analyze("Not great") in ["Bad", "Neutral"]
    
    # Extreme negative
    assert analyzer.analyze("I hate this so much!") in ["Very Bad", "Bad"]

