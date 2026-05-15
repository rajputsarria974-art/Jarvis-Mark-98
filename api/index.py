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
        .main-container { border: 1px solid #00f2ff; width: 90%; max-width: 500px; height: 70vh; border-radius: 10px; padding: 20px; display: flex; flex-direction: column; background: #050505; box-shadow: 0 0 15px #00f2ff; }
        #display { flex-grow: 1; overflow-y: auto; text-align: left; padding: 10px; font-size: 16px; scrollbar-width: none; }
        input { width: 100%; padding: 12px; background: #111; border: 1px solid #00f2ff; color: #fff; border-radius: 5px; outline: none; box-sizing: border-box; }
        .pulse { height: 8px; width: 8px; background: #00f2ff; border-radius: 50%; display: inline-block; animation: blink 1.5s infinite; }
        @keyframes blink { 0% { opacity: 0.3; } 50% { opacity: 1; } 100% { opacity: 0.3; } }
    </style>
</head>
<body>
    <div class="main-container">
        <div style="font-size: 12px; margin-bottom: 10px;"><span class="pulse"></span> CONNECTED TO CORE</div>
        <div id="display">Awaiting command, Sir Arslan...</div>
        <input type="text" id="userInput" placeholder="Enter command..." onkeypress="if(event.key==='Enter') send()">
    </div>
    <script>
        async function send() {
            let input = document.getElementById('userInput');
            let display = document.getElementById('display');
            let msg = input.value;
            if(!msg) return;
            display.innerHTML += `<div style="color:#888; margin-top:10px;">> ${msg}</div>`;
            input.value = '';
            try {
                let res = await fetch('/chat?msg=' + encodeURIComponent(msg));
                let data = await res.json();
                display.innerHTML += `<div style="color:#00f2ff; margin-top:5px;"><b>JARVIS:</b> ${data.reply}</div>`;
            } catch (e) {
                display.innerHTML += `<div style="color:red;">SIGNAL LOST. RECONNECTING...</div>`;
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
    # Switching to Google Gemma 2B (Very light and fast)
    API_URL = "https://api-inference.huggingface.co/models/google/gemma-1.1-2b-it"
    headers = {"Authorization": f"Bearer {HF_KEY}"}
    
    payload = {
        "inputs": f"User: {msg}\nAssistant: You are JARVIS, Sir Arslan's AI. Answer in 1 short sentence.",
        "parameters": {"max_new_tokens": 50, "wait_for_model": True}
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=12)
        result = response.json()
        
        if isinstance(result, list):
            reply = result[0]['generated_text'].split("Assistant:")[-1].strip()
        elif 'error' in result:
            reply = "Sir, the server is under heavy load. Please send the command again."
        else:
            reply = "Core initialized. Ready for next task."
            
        return jsonify({"reply": reply})
    except:
        return jsonify({"reply": "Satellite link unstable. Standing by."})
