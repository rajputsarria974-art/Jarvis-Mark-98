import os
import requests
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# ✅ APNI STABLE HUGGING FACE KEY (Token)
HF_KEY = "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"

HTML_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>JARVIS MARK-100</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { 
            background: #000 url('http://googleusercontent.com/image_collection/image_retrieval/688826044006652512_1') no-repeat center center fixed; 
            background-size: cover;
            color: #00f2ff; 
            font-family: 'Segoe UI', sans-serif; 
            text-align: center; 
            margin: 0;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .glass-panel {
            background: rgba(0, 15, 30, 0.85);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(0, 242, 255, 0.4);
            width: 90%;
            max-width: 500px;
            height: 80vh;
            border-radius: 25px;
            padding: 20px;
            box-shadow: 0 0 50px rgba(0, 242, 255, 0.3);
            display: flex;
            flex-direction: column;
        }
        h2 { margin: 10px 0; letter-spacing: 5px; text-transform: uppercase; }
        #display {
            flex-grow: 1;
            overflow-y: auto;
            padding: 15px;
            text-align: left;
            font-size: 15px;
            scrollbar-width: none;
        }
        input {
            width: 100%;
            padding: 15px;
            background: rgba(0, 0, 0, 0.7);
            border: 1px solid #00f2ff;
            border-radius: 50px;
            color: #fff;
            font-size: 16px;
            outline: none;
            box-sizing: border-box;
        }
        .arc-reactor {
            width: 60px;
            height: 60px;
            border: 3px double #00f2ff;
            border-radius: 50%;
            margin: 0 auto;
            animation: pulse 2s infinite ease-in-out;
        }
        @keyframes pulse {
            0% { transform: scale(1); box-shadow: 0 0 10px #00f2ff; }
            50% { transform: scale(1.05); box-shadow: 0 0 30px #00f2ff; }
            100% { transform: scale(1); box-shadow: 0 0 10px #00f2ff; }
        }
    </style>
</head>
<body>
    <div class="glass-panel">
        <div class="arc-reactor"></div>
        <h2>J.A.R.V.I.S.</h2>
        <div id="display">
            <div style="color:#00f2ff;">SYSTEM SECURE. READY FOR YOUR COMMANDS, SIR ARSLAN.</div>
        </div>
        <div style="padding-top: 15px;">
            <input type="text" id="userInput" placeholder="Listening..." onkeypress="if(event.key==='Enter') send()">
        </div>
    </div>

    <script>
        async function send() {
            let input = document.getElementById('userInput');
            let display = document.getElementById('display');
            let msg = input.value;
            if(!msg) return;

            display.innerHTML += `<div style="color:#fff; margin-top:10px;"><b>Arslan:</b> ${msg}</div>`;
            input.value = '';
            display.scrollTop = display.scrollHeight;
            
            try {
                let res = await fetch('/chat?msg=' + encodeURIComponent(msg));
                let data = await res.json();
                display.innerHTML += `<div style="color:#00f2ff; margin-top:10px;"><b>JARVIS:</b> ${data.reply}</div>`;
            } catch (e) {
                display.innerHTML += `<div style="color:red;">CONNECTION LOST.</div>`;
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
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
    headers = {"Authorization": f"Bearer {HF_KEY}"}
    
    payload = {
        "inputs": f"<s>[INST] You are JARVIS, the personal AI assistant for Sir Arslan. Keep answers very short and loyal. Question: {msg} [/INST]",
        "parameters": {"max_new_tokens": 100}
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=15)
        result = response.json()
        reply = result[0]['generated_text'].split("[/INST]")[-1].strip()
        return jsonify({"reply": reply})
    except:
        return jsonify({"reply": "Sir, internal circuits are stable but the satellite link is slow. Please re-send."})
