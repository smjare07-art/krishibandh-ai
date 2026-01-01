from flask import Flask, request, jsonify, make_response
import requests
import os
from flask_cors import CORS

app = Flask(__name__)

# ✅ STRICT + SAFE CORS CONFIG (NULL ORIGIN INCLUDED)
CORS(
    app,
    resources={r"/*": {"origins": "*"}},
    supports_credentials=False
)

HF_API_KEY = os.getenv("HF_API_KEY")
HF_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response


@app.route("/", methods=["GET"])
def home():
    return "Krishibandh AI Backend Running ✅"


@app.route("/crop-advice", methods=["POST", "OPTIONS"])
def crop_advice():

    # ✅ HANDLE PREFLIGHT MANUALLY
    if request.method == "OPTIONS":
        return make_response("", 200)

    data = request.get_json(force=True)
    text = data.get("text", "")

    headers = {
        "Authorization": f"Bearer {HF_API_KEY}"
    }

    payload = {
        "inputs": text
    }

    hf_response = requests.post(HF_URL, headers=headers, json=payload, timeout=60)
    return jsonify(hf_response.json())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
