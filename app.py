from flask import Flask, request, jsonify, make_response
import requests
import os

app = Flask(__name__)

HF_API_KEY = os.getenv("HF_API_KEY")
HF_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"


# ✅ GLOBAL CORS HEADERS (MOST IMPORTANT)
@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add(
        "Access-Control-Allow-Headers",
        "Content-Type, Authorization"
    )
    response.headers.add(
        "Access-Control-Allow-Methods",
        "GET, POST, OPTIONS"
    )
    return response


@app.route("/", methods=["GET"])
def home():
    return "Krishibandh AI Backend Running ✅"


# ✅ HANDLE OPTIONS SEPARATELY (NO JSON TOUCH)
@app.route("/crop-advice", methods=["OPTIONS"])
def crop_advice_options():
    return make_response("", 204)


# ✅ ACTUAL POST ENDPOINT
@app.route("/crop-advice", methods=["POST"])
def crop_advice():

    # ⚠️ force=False to avoid 415
    data = request.get_json(silent=True)
    text = data.get("text", "") if data else ""

    headers = {
        "Authorization": f"Bearer {HF_API_KEY}"
    }

    payload = {
        "inputs": text
    }

    hf_response = requests.post(
        HF_URL,
        headers=headers,
        json=payload,
        timeout=60
    )

    return jsonify(hf_response.json())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
