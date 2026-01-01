from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

HF_API_KEY = os.getenv("HF_API_KEY")
HF_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"

@app.route("/")
def home():
    return "Krishibandh AI Backend Running ✅"

@app.route("/crop-advice", methods=["POST"])
def crop_advice():
    data = request.get_json()
    text = data.get("text", "")

    headers = {
        "Authorization": f"Bearer {HF_API_KEY}"
    }

    payload = {
        "inputs": text
    }

    response = requests.post(HF_URL, headers=headers, json=payload)
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

