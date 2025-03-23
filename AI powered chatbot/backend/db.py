import json
import threading
import logging
import os

FAQ_FILE = os.path.join(os.path.dirname(__file__), "../database/faq_data.json")

# Logging setup
logging.basicConfig(
    filename="database.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class DatabaseConnection:
    """A thread-safe, singleton JSON database manager."""
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        """Ensure only one instance is created (Singleton Pattern)."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(DatabaseConnection, cls).__new__(cls)
                    cls._instance._load_data()
        return cls._instance

    def _load_data(self):
        """Load FAQ data from the JSON file."""
        try:
            if not os.path.exists(FAQ_FILE):
                logging.warning("FAQ file missing, creating default file.")
                self.faq_data = []
                self._save_data()
            else:
                with open(FAQ_FILE, "r", encoding="utf-8") as file:
                    self.faq_data = json.load(file)
                logging.info("FAQ data loaded successfully.")
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logging.error(f"Failed to load FAQ data: {str(e)}")
            self.faq_data = []

    def _save_data(self):
        """Save FAQ data to the JSON file."""
        try:
            with open(FAQ_FILE, "w", encoding="utf-8") as file:
                json.dump(self.faq_data, file, indent=4)
            logging.info("FAQ data saved successfully.")
        except Exception as e:
            logging.error(f"Error saving FAQ data: {str(e)}")

    def get_faq_data(self):
        """Return the loaded FAQ data."""
        return self.faq_data

    def add_faq_entry(self, question, answer):
        """Add a new FAQ entry and save it to the database."""
        self.faq_data.append({"question": question, "answer": answer})
        self._save_data()

# Function to get FAQ data
def get_faq_data():
    """Helper function to fetch FAQ data."""
    return DatabaseConnection().get_faq_data()
