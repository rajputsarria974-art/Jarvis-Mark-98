import os
import requests
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# ✅ ARSLAN INDUSTRIES - STABLE KEY
HF_KEY = "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"

HTML_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>JARVIS MARK-100</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { background: #000; color: #00f2ff; font-family: 'Segoe UI', sans-serif; margin: 0; height: 100vh; display: flex; justify-content: center; align-items: center; }
        .main-container { border: 2px solid #00f2ff; width: 90%; max-width: 500px; height: 80vh; border-radius: 20px; padding: 20px; display: flex; flex-direction: column; background: rgba(0, 5, 15, 0.95); box-shadow: 0 0 30px #00f2ff; }
        #display { flex-grow: 1; overflow-y: auto; text-align: left; padding: 10px; scrollbar-width: none; }
        input { width: 100%; padding: 15px; background: #000; border: 1px solid #00f2ff; color: #fff; border-radius: 50px; outline: none; box-sizing: border-box; margin-top: 10px; }
        .arc { width: 45px; height: 45px; border: 2px solid #00f2ff; border-radius: 50%; margin: 0 auto 10px; animation: pulse 2s infinite ease-in-out; }
        @keyframes pulse { 0% { transform: scale(1); box-shadow: 0 0 10px #00f2ff; } 50% { transform: scale(1.1); box-shadow: 0 0 25px #00f2ff; } 100% { transform: scale(1); box-shadow: 0 0 10px #00f2ff; } }
    </style>
</head>
<body>
    <div class="main-container">
        <div class="arc"></div>
        <div style="font-size: 10px; text-align: center; letter-spacing: 2px;">RENDER CORE ACTIVE</div>
        <div id="display">SYSTEM ONLINE. STANDING BY, SIR ARSLAN.</div>
        <input type="text" id="userInput" placeholder="Listening..." onkeypress="if(event.key==='Enter') send()">
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
                display.innerHTML += `<div style="color:#00f2ff; margin-top:10px;"><b>JARVIS:</b> ${data.reply}</div>`;
            } catch (e) {
                display.innerHTML += `<div style="color:red;">CORE ERROR.</div>`;
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
    # Using TinyLlama for speed on Render
    API_URL = "https://api-inference.huggingface.co/models/TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    headers = {"Authorization": f"Bearer {HF_KEY}"}
    payload = {"inputs": f"<|system|>You are JARVIS, Sir Arslan's loyal AI.<|user|>{msg}<|assistant|>"}
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=15)
        result = response.json()
        reply = result[0]['generated_text'].split("<|assistant|>")[-1].strip()
        return jsonify({"reply": reply})
    except:
        return jsonify({"reply": "Sir, server is syncing. Please wait a moment."})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
