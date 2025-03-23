from db import DatabaseConnection
from model import NLPModel
import random
import logging
import openai  # Used for GPT fallback responses

# Logging setup
logging.basicConfig(
    filename="chatbot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class Chatbot:
    """Main chatbot logic integrating NLP and database operations."""
    
    def __init__(self):
        self.db = DatabaseConnection()
        self.nlp = NLPModel()
        self.faq_data = self.db.get_faq_data()
        self.nlp.build_faiss_index(self.faq_data)

    def get_response(self, user_input):
        """Processes user input and returns an appropriate response."""
        response = self.query_exact_match(user_input) or self.query_semantic_match(user_input)

        if not response:
            response = self.generate_fallback_response(user_input)
        
        return response

    def query_exact_match(self, user_input):
        """Finds an exact match in the FAQ database."""
        for entry in self.faq_data:
            if user_input.lower() == entry["question"].lower():
                return entry["answer"]
        return None

    def query_semantic_match(self, user_input):
        """Finds the closest match using FAISS vector search."""
        best_match, distance = self.nlp.find_similar_question(user_input)

        if best_match and distance < 5.0:  # Lower distance = better match
            for entry in self.faq_data:
                if entry["question"] == best_match:
                    return entry["answer"]
        return None

    def generate_fallback_response(self, user_input):
        """Generates fallback responses using GPT or predefined answers."""
        predefined_fallbacks = [
            "I'm not sure about that. Can you rephrase?",
            "I couldn't find an exact answer. Would you like to contact support?",
        ]
        return random.choice(predefined_fallbacks)

# Usage Example
chatbot = Chatbot()
user_query = "How do I reset my password?"
response = chatbot.get_response(user_query)
print(response)
