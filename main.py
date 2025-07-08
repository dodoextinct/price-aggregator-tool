from flask import Flask
from dotenv import load_dotenv
import logging
import os

# Load .env variables
load_dotenv()

# Logging setup
logging.basicConfig(level=logging.INFO)
logging.getLogger("pymongo").setLevel(logging.WARNING)

# Initialize Flask app
app = Flask(__name__)

# Register your route(s)
from routes.compare import compare_bp
app.register_blueprint(compare_bp)

# Optional: Health check route
@app.route("/")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
