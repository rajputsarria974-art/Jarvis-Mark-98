import os, requests
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)
HF_KEY = "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"

@app.route('/')
def home():
    return "<h1>Jarvis System Online</h1><p>Send a message to /chat?msg=hello</p>"

@app.route('/chat')
def chat():
    msg = request.args.get('msg')
    # TinyLlama: Sab se chota aur fast model
    API_URL = "https://api-inference.huggingface.co/models/TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    headers = {"Authorization": f"Bearer {HF_KEY}"}
    payload = {"inputs": f"<|system|>You are JARVIS. Answer short.<|user|>{msg}<|assistant|>"}
    
    try:
        # wait_for_model=True isay line mein laga dega taake error na aaye
        response = requests.post(API_URL, headers=headers, json=payload, params={"wait_for_model": True}, timeout=20)
        result = response.json()
        reply = result[0]['generated_text'].split("<|assistant|>")[-1].strip()
        return jsonify({"reply": reply})
    except:
        return jsonify({"reply": "Sir, Hugging Face servers are overloaded. Should we switch back to SambaNova?"})
