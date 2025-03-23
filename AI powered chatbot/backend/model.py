import spacy
import logging
import faiss
import numpy as np

# Logging setup
logging.basicConfig(
    filename="nlp.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class NLPModel:
    """Advanced NLP Model for text preprocessing and keyword extraction."""
    
    _nlp = None  # Lazy loading of the NLP model

    def __init__(self, model_name="en_core_web_md"):
        """Load the spaCy model only when required."""
        if NLPModel._nlp is None:
            try:
                NLPModel._nlp = spacy.load(model_name)
                logging.info(f"Loaded NLP model: {model_name}")
            except Exception as e:
                logging.error(f"Error loading NLP model: {str(e)}")
                raise

        self.nlp = NLPModel._nlp
        self.custom_stopwords = set()  # Allows adding/removing stopwords dynamically
        self.index = None
        self.faq_embeddings = []
        self.faq_questions = []

    def preprocess(self, text):
        """Preprocess text: lowercasing, lemmatization, and stopword removal."""
        doc = self.nlp(text.lower().strip())
        return " ".join([token.lemma_ for token in doc if token.is_alpha and token.text not in self.custom_stopwords])

    def extract_keywords(self, text, top_n=5):
        """Extracts important keywords from the text."""
        doc = self.nlp(text.lower())
        keywords = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]
        return list(set(keywords))[:top_n]  # Return top N unique keywords

    def extract_entities(self, text):
        """Extract named entities like names, dates, organizations, etc."""
        doc = self.nlp(text)
        entities = {ent.label_: ent.text for ent in doc.ents}
        return entities if entities else "No entities found."

    def add_stopwords(self, words):
        """Dynamically add custom stopwords."""
        self.custom_stopwords.update(words)

    def remove_stopwords(self, words):
        """Dynamically remove custom stopwords."""
        self.custom_stopwords.difference_update(words)

    def build_faiss_index(self, faq_data):
        """Builds FAISS index for semantic search."""
        self.faq_questions = [entry["question"] for entry in faq_data]
        self.faq_embeddings = [self.nlp(q).vector for q in self.faq_questions]

        if self.faq_embeddings:
            self.index = faiss.IndexFlatL2(len(self.faq_embeddings[0]))
            self.index.add(np.array(self.faq_embeddings))
            logging.info("FAISS index built successfully.")

    def find_similar_question(self, query):
        """Finds the most similar FAQ question using FAISS."""
        if self.index is None:
            return None, 0

        query_vector = np.array([self.nlp(query).vector])
        D, I = self.index.search(query_vector, 1)  # Find the closest match
        return self.faq_questions[I[0][0]], D[0][0]  # Return the closest question and its score
