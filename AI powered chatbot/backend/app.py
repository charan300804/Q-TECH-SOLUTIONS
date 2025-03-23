from flask import Flask, request, jsonify, abort, render_template
from flask_cors import CORS
import logging
import threading
import time
import redis
import json
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_limiter.errors import RateLimitExceeded
import warnings
import signal
import sys
import os

# Suppress in-memory rate limit warnings for local development
warnings.filterwarnings("ignore", category=UserWarning, module="flask_limiter")

# ✅ Initialize Flask app with correct frontend paths
app = Flask(
    __name__,
    template_folder="../frontend/templates",  # Ensure correct path
    static_folder="../frontend/static"
)

# Enable CORS (Allow all origins temporarily for debugging)
CORS(app)

# ✅ Configure logging
logging.basicConfig(
    filename="chatbot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a",
)

# ✅ Try connecting to Redis for rate limiting
redis_client = None
storage_uri = "memory://"  # Default to in-memory if Redis fails

try:
    redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
    redis_client.ping()
    logging.info("✅ Redis connection established.")
    storage_uri = "redis://localhost:6379/0"
except redis.exceptions.ConnectionError:
    logging.warning("⚠️ Redis not available. Falling back to in-memory rate limiting.")

# ✅ Setup rate limiting (Defaults to in-memory if Redis is unavailable)
limiter = Limiter(get_remote_address, app=app, storage_uri=storage_uri)

# ✅ Load FAQ data from JSON file
FAQ_FILE = os.path.join(os.path.dirname(__file__), "../backend/database/faq_data.json")  # Ensure correct path

def load_faq_data():
    """Load FAQs from the JSON file."""
    try:
        if not os.path.exists(FAQ_FILE):
            logging.error(f"❌ FAQ file not found: {FAQ_FILE}")
            return []
        with open(FAQ_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        logging.error("❌ Failed to parse JSON data. Check the FAQ file format.")
        return []
    except Exception as e:
        logging.error(f"❌ Unexpected error loading FAQ data: {str(e)}")
        return []

faq_data = load_faq_data()

def find_answer(user_input):
    """Finds the best-matching answer in the FAQ data."""
    user_input = user_input.lower()
    for faq in faq_data:
        if user_input in faq["question"].lower():
            return faq["answer"]
    return "I'm sorry, I couldn't find an answer to your question."

# ✅ Serve the frontend UI
@app.route("/")
def home():
    """Render the chatbot UI."""
    try:
        logging.info("✅ Home page accessed")
        return render_template("index.html")  # Ensure it exists in templates/
    except Exception as e:
        logging.error(f"❌ Error loading home page: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route("/chat", methods=["POST"])
@limiter.limit("3 per 10 seconds")  # Apply rate limiting
def chat():
    """Handles user messages and returns chatbot responses."""
    try:
        data = request.get_json()

        # Validate request
        if not data or "message" not in data:
            logging.warning("400 - Bad Request: Missing 'message' field.")
            return jsonify({"error": "Missing 'message' in request"}), 400

        user_input = data["message"].strip()
        if not user_input:
            logging.warning("400 - Bad Request: Empty message received.")
            return jsonify({"error": "Empty message received"}), 400

        # Find chatbot response
        response = find_answer(user_input)
        logging.info(f"User: {user_input} | Bot: {response}")

        return jsonify({"response": response})
    
    except Exception as e:
        logging.error(f"500 - Internal Server Error: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

# ✅ Handle Rate Limit Exceeded
@app.errorhandler(RateLimitExceeded)
def rate_limit_exceeded(e):
    logging.warning(f"429 - Rate Limit Exceeded: {e.description}")
    return jsonify({"error": "Too many requests, slow down!"}), 429

# ✅ Validate JSON before requests
@app.before_request
def validate_json():
    if request.method == "POST" and not request.is_json:
        abort(400, description="Request must be JSON")

# ✅ Background Task for Periodic Logging
def background_task():
    """A background task that runs in a separate thread every 60 seconds."""
    while True:
        logging.info("⏳ Background task running...")
        time.sleep(60)  # Execute every 60 seconds

# Start a background monitoring thread
thread = threading.Thread(target=background_task, daemon=True)
thread.start()

# ✅ Graceful Shutdown Handler
def shutdown_handler(signal, frame):
    logging.info("🔴 Shutting down gracefully...")
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown_handler)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))  # Allow dynamic port selection
    debug_mode = os.getenv("DEBUG", "True").lower() == "true"

    logging.info(f"🚀 Starting Flask server on port {port}, debug={debug_mode}")
    app.run(host="0.0.0.0", port=port, threaded=True, debug=debug_mode)
'''
1. General Information  
2. Account & Login  
3. Payment & Billing  
4. Product & Services  
5. Technical Support  
6. Privacy & Security  
7. Shipping & Delivery  
8. Returns & Refunds  
9. Customer Support  
10. Business & Partnership  
11. Subscription & Membership  
12. Order Tracking  
13. Cancellation Policy  
14. Troubleshooting Errors  
15. Software Installation  
16. Warranty & Repairs  
17. User Permissions & Access  
18. Career & Job Opportunities  
19. Discounts & Promotions  
20. Gift Cards & Vouchers  
21. Mobile App Support  
22. Terms & Conditions  
23. Data Protection & GDPR  
24. Social Media & Community  
25. Affiliate Programs  
26. Loyalty Programs  
27. Complaint & Feedback Handling  
28. Legal & Compliance  
29. International Shipping  
30. Vendor & Supplier Inquiries  
31. Accessibility & Usability  
32. Customization & Personalization  
33. Service Outages & Downtime  
34. API Documentation & Support  
35. Multi-Language Support  
36. Product Compatibility  
37. Environmental & Sustainability Policies  
38. Event & Webinar Registration  
39. Press & Media Inquiries  
40. Industry-Specific Regulations  
41. Pricing & Cost Estimation  
42. Open-Source & Licensing  
43. Software Updates & Patches  
44. Fraud & Scam Awareness  
45. Emergency & Disaster Support  
46. Health & Safety Guidelines  
47. Training & Certification  
48. Community Forums & Discussions  
49. Contact Information & Helpline  
50. Innovations & Future Developments'''