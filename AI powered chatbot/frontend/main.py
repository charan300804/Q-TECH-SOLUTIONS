from flask import Flask, render_template, jsonify, request
import logging
import os

# Initialize Flask app
app = Flask(__name__, static_folder="static", template_folder="templates")

# Ensure log directory exists
log_file = "app.log"
if not os.path.exists(log_file):
    open(log_file, "a").close()  # Create the file if it doesn't exist

# Configure logging
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

@app.before_request
def log_request():
    """Log every request with the requester's IP."""
    if request.path.startswith("/static/"):
        return  # Ignore logging for static files to reduce noise
    app.logger.info(f"Request from {request.remote_addr} to {request.path}")

@app.route("/")
def home():
    """Render the chatbot UI."""
    try:
        app.logger.info("✅ Home page accessed")
        return render_template("index.html")
    except Exception as e:
        app.logger.error(f"❌ Error loading home page: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors gracefully."""
    app.logger.warning(f"⚠️ 404 Error - Page not found: {request.path}")

    # Check if the 404 template exists before rendering
    error_page = "404.html"
    error_page_path = os.path.join(app.template_folder, error_page)

    if not os.path.exists(error_page_path):
        app.logger.error(f"❌ Missing template: {error_page}")
        return jsonify({"error": "Page not found"}), 404

    return render_template(error_page), 404

@app.errorhandler(500)
def server_error(error):
    """Handle server errors gracefully."""
    app.logger.error(f"🔥 500 Error - Internal Server Error: {error}")

    # Check if the 500 template exists before rendering
    error_page = "500.html"
    error_page_path = os.path.join(app.template_folder, error_page)

    if not os.path.exists(error_page_path):
        app.logger.error(f"❌ Missing template: {error_page}")
        return jsonify({"error": "Something went wrong. Please try again later."}), 500

    return render_template(error_page), 500

if __name__ == "__main__":
    # Fetch port & debug mode from environment variables (default: port=5001, debug=True)
    port = int(os.getenv("PORT", 5001))
    debug_mode = os.getenv("DEBUG", "True").lower() == "true"

    app.logger.info(f"🚀 Starting Flask server on port {port}, debug={debug_mode}")
    app.logger.info(f"📂 Template folder path: {os.path.abspath(app.template_folder)}")

    try:
        app.run(host="0.0.0.0", port=port, debug=debug_mode)
    except Exception as e:
        app.logger.error(f"❌ Failed to start server: {str(e)}")
