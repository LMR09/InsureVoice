"""
InsureVoice — AI Sentiment Analysis Backend
============================================
Framework : Flask
NLP        : TextBlob + NLTK
Run locally: python app.py
Run in prod: gunicorn app:app

Endpoints:
  POST /analyze          — analyze a single review text
  POST /analyze/batch    — analyze multiple texts
  GET  /health           — health check
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import os
from sentiment import analyze_sentiment, batch_analyze

app = Flask(__name__)

# ── Allow requests from any origin (CORS) ──
# In production, replace "*" with your Vercel URL:
# CORS(app, origins=["https://your-app.vercel.app"])
CORS(app, origins="*")


# ═══════════════════════════════════════════
#  ROUTES
# ═══════════════════════════════════════════

@app.route("/health", methods=["GET"])
def health():
    """Health check — used by frontend to test if backend is running."""
    return jsonify({"status": "ok", "service": "InsureVoice Sentiment API"}), 200

@app.route("/")
def home():
    return {
        "status": "success",
        "message": "InsureVoice Sentiment API Running"
    }

@app.route("/analyze", methods=["POST"])
def analyze():
    """
    Analyze sentiment of a single review text.

    Request body (JSON):
        { "text": "The claim was rejected without reason." }

    Response (JSON):
        {
          "sentiment":    "negative",
          "polarity":     -0.45,
          "subjectivity": 0.72,
          "label":        "Negative 😞",
          "confidence":   "high",
          "keywords": {
            "positive": ["..."],
            "negative": ["rejected", "without"]
          }
        }
    """
    data = request.get_json(silent=True)

    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' field in request body."}), 400

    text = data["text"].strip()

    if not text:
        return jsonify({"error": "Text cannot be empty."}), 400

    if len(text) > 10000:
        return jsonify({"error": "Text too long. Maximum 10,000 characters."}), 400

    try:
        result = analyze_sentiment(text)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/analyze/batch", methods=["POST"])
def analyze_batch():
    """
    Analyze multiple reviews at once.

    Request body (JSON):
        { "texts": ["text1", "text2", ...] }

    Response (JSON):
        { "results": [{ ...sentiment_result }, ...] }
    """
    data = request.get_json(silent=True)

    if not data or "texts" not in data:
        return jsonify({"error": "Missing 'texts' field."}), 400

    texts = data["texts"]

    if not isinstance(texts, list):
        return jsonify({"error": "'texts' must be an array."}), 400

    if len(texts) > 50:
        return jsonify({"error": "Maximum 50 texts per batch."}), 400

    try:
        results = batch_analyze(texts)
        return jsonify({"results": results}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ═══════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"\n🚀 InsureVoice Sentiment API running at http://localhost:{port}")
    print("   Test: POST /analyze  { \"text\": \"Your review here\" }\n")
    app.run(host="0.0.0.0", port=port, debug=True)
