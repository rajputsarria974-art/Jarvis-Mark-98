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
        /* Lightweight Animations for better performance on Asus X52J */
        body { 
            background: #000; 
            color: #00f2ff; 
            font-family: 'Segoe UI', sans-serif; 
            margin: 0;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .main-container {
            border: 2px solid #00f2ff;
            width: 90%;
            max-width: 500px;
            height: 80vh;
            border-radius: 15px;
            padding: 15px;
            display: flex;
            flex-direction: column;
            background: rgba(0, 20, 40, 0.9);
            box-shadow: 0 0 20px #00f2ff;
        }
        #display {
            flex-grow: 1;
            overflow-y: auto;
            text-align: left;
            padding: 10px;
            font-size: 16px;
        }
        input {
            width: 100%;
            padding: 12px;
            background: #000;
            border: 1px solid #00f2ff;
            color: #fff;
            border-radius: 5px;
            outline: none;
        }
        .status-dot {
            height: 10px;
            width: 10px;
            background-color: #00f2ff;
            border-radius: 50%;
            display: inline-block;
            animation: blink 1s infinite;
        }
        @keyframes blink { 0% { opacity: 0.2; } 50% { opacity: 1; } 100% { opacity: 0.2; } }
    </style>
</head>
<body>
    <div class="main-container">
        <div style="text-align: left;"><span class="status-dot"></span> JARVIS CORE ONLINE</div>
        <div id="display">READY FOR INPUT, SIR ARSLAN.</div>
        <input type="text" id="userInput" placeholder="Command..." onkeypress="if(event.key==='Enter') send()">
    </div>

    <script>
        async function send() {
            let input = document.getElementById('userInput');
            let display = document.getElementById('display');
            let msg = input.value;
            if(!msg) return;

            display.innerHTML += `<div style="color:#fff; margin-top:5px;"><b>Arslan:</b> ${msg}</div>`;
            input.value = '';
            
            try {
                let res = await fetch('/chat?msg=' + encodeURIComponent(msg));
                let data = await res.json();
                display.innerHTML += `<div style="color:#00f2ff; margin-top:5px;"><b>JARVIS:</b> ${data.reply}</div>`;
            } catch (e) {
                display.innerHTML += `<div style="color:red;">SYSTEM OVERLOAD. RETRYING...</div>`;
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
    # Use a very light model for speed
    API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
    headers = {"Authorization": f"Bearer {HF_KEY}"}
    
    payload = {
        "inputs": f"<|system|>You are JARVIS. Speak briefly.<|user|>{msg}<|assistant|>",
        "parameters": {"max_new_tokens": 50}
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=8)
        result = response.json()
        reply = result[0]['generated_text'].split("<|assistant|>")[-1].strip()
        return jsonify({"reply": reply})
    except:
        return jsonify({"reply": "Sir, server is busy. Please try one more time."})
