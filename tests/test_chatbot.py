import os
import pytest # type: ignore
from app.chatbot import ChatBot

@pytest.fixture
def bot():
    return ChatBot()

def test_keyword_responses(bot):
    # These should return one of the predefined responses
    hello_response = bot.get_response("hello")
    assert hello_response in bot.keyword_responses["hello"]

    bye_response = bot.get_response("bye")
    assert bye_response in bot.keyword_responses["bye"]

def test_case_insensitivity(bot):
    # Check if uppercase input works
    response = bot.get_response("HELLO")
    assert response in bot.keyword_responses["hello"]

def test_markov_fallback(bot):
    # Simulate input that does not match keywords
    response = bot.get_response("random input not in keywords")
    assert response is not None
    assert isinstance(response, str)
    assert len(response) > 0

def test_empty_input(bot):
    # Should return fallback message
    response = bot.get_response("")
    assert response == "Sorry, I couldn't hear you clearly."
