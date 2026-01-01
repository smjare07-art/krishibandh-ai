from flask import Flask, request, jsonify, make_response
import requests
import os
import random

app = Flask(__name__)

# ======================
# CONFIG
# ======================
HF_API_KEY = os.getenv("HF_API_KEY")

# 🔥 FAST + STABLE FREE MODEL
HF_URL = "https://api-inference.huggingface.co/models/google/flan-t5-small"

# 🟢 FALLBACK ADVICE (ALWAYS WORKS)
FALLBACK_ADVICE = [
    "🌱 पिकाची नियमित पाहणी करा.",
    "💧 पाणी साचू देऊ नका.",
    "🐛 रोगट पाने काढून नष्ट करा.",
    "🌾 संतुलित खतांचा वापर करा.",
    "📞 जवळच्या कृषी अधिकाऱ्यांचा सल्ला घ्या."
]

# ======================
# CORS (HARD FIX)
# ======================
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response

# ======================
# ROUTES
# ======================
@app.route("/", methods=["GET"])
def home():
    return "Krishibandh AI Backend Running ✅"

# OPTIONS (preflight)
@app.route("/crop-advice", methods=["OPTIONS"])
def crop_advice_options():
    return make_response("", 204)

# MAIN API
@app.route("/crop-advice", methods=["POST"])
def crop_advice():
    data = request.get_json(silent=True)
    text = data.get("text", "") if data else ""

    headers = {
        "Authorization": f"Bearer {HF_API_KEY}"
    }

    payload = {
        "inputs": text
    }

    try:
        hf_response = requests.post(
            HF_URL,
            headers=headers,
            json=payload,
            timeout=40
        )

        if hf_response.status_code == 200:
            return jsonify(hf_response.json())

    except Exception:
        pass

    # 🔁 FALLBACK (NO FAILURE SHOWN TO USER)
    return jsonify([{
        "generated_text": random.choice(FALLBACK_ADVICE)
    }])

# ======================
# START
# ======================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
