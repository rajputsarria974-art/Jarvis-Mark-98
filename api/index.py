import os
import requests
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# ✅ ARSLAN INDUSTRIES STABLE KEY
HF_KEY = "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"

HTML_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>JARVIS MARK-100</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { background: #000; color: #00f2ff; font-family: 'Segoe UI', sans-serif; margin: 0; height: 100vh; display: flex; justify-content: center; align-items: center; }
        .main-container { border: 1px solid #00f2ff; width: 90%; max-width: 500px; height: 75vh; border-radius: 15px; padding: 20px; display: flex; flex-direction: column; background: rgba(0, 10, 20, 0.9); box-shadow: 0 0 20px #00f2ff; }
        #display { flex-grow: 1; overflow-y: auto; text-align: left; padding: 10px; font-size: 16px; border-bottom: 1px solid rgba(0,242,255,0.2); }
        input { width: 100%; padding: 15px; background: #000; border: 1px solid #00f2ff; color: #fff; border-radius: 50px; outline: none; box-sizing: border-box; margin-top: 15px; }
        .status { font-size: 12px; color: #00f2ff; text-transform: uppercase; letter-spacing: 2px; }
    </style>
</head>
<body>
    <div class="main-container">
        <div class="status">● System Online</div>
        <div id="display">Welcome back, Sir Arslan. System is at your disposal.</div>
        <input type="text" id="userInput" placeholder="Command..." onkeypress="if(event.key==='Enter') send()">
    </div>
    <script>
        async function send() {
            let input = document.getElementById('userInput');
            let display = document.getElementById('display');
            let msg = input.value;
            if(!msg) return;
            display.innerHTML += `<div style="color:#fff; margin-top:10px;"><b>Arslan:</b> ${msg}</div>`;
            input.value = '';
            try {
                let res = await fetch('/chat?msg=' + encodeURIComponent(msg));
                let data = await res.json();
                display.innerHTML += `<div style="color:#00f2ff; margin-top:5px;"><b>JARVIS:</b> ${data.reply}</div>`;
            } catch (e) {
                display.innerHTML += `<div style="color:red;">ERROR: Signal Interrupted.</div>`;
            }
            display.scrollTop = display.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_UI)

@app.route('/chat')
def chat():
    msg = request.args.get('msg')
    # TinyLlama: Best for free tier speed
    API_URL = "https://api-inference.huggingface.co/models/TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    headers = {"Authorization": f"Bearer {HF_KEY}"}
    payload = {"inputs": f"<|system|>You are JARVIS, Sir Arslan's loyal AI. Short answers only.<|user|>{msg}<|assistant|>"}
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, params={"wait_for_model": True}, timeout=15)
        result = response.json()
        reply = result[0]['generated_text'].split("<|assistant|>")[-1].strip()
        return jsonify({"reply": reply})
    except:
        return jsonify({"reply": "Sir, server is syncing. Please repeat the command."})
