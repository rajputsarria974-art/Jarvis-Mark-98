import os
import requests
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# ✅ ARSLAN INDUSTRIES - VERIFIED SAMBANOVA KEY
SAMBA_KEY = "a9f227f9-1a48-4a63-81bf-606a7fee5adf"

HTML_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>JARVIS MARK-100</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { 
            background: #000; 
            color: #00f2ff; 
            font-family: 'Segoe UI', sans-serif; 
            margin: 0; 
            height: 100vh; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            overflow: hidden;
        }
        .main-container { 
            border: 2px solid #00f2ff; 
            width: 90%; 
            max-width: 500px; 
            height: 85vh; 
            border-radius: 20px; 
            padding: 20px; 
            display: flex; 
            flex-direction: column; 
            background: rgba(0, 5, 15, 0.95); 
            box-shadow: 0 0 30px rgba(0, 242, 255, 0.4); 
        }
        #display { 
            flex-grow: 1; 
            overflow-y: auto; 
            text-align: left; 
            padding: 10px; 
            font-size: 16px; 
            scrollbar-width: none;
            border-bottom: 1px solid rgba(0, 242, 255, 0.1);
        }
        #display::-webkit-scrollbar { display: none; }
        .input-box { padding-top: 15px; }
        input { 
            width: 100%; 
            padding: 15px; 
            background: rgba(0, 242, 255, 0.05); 
            border: 1px solid #00f2ff; 
            color: #fff; 
            border-radius: 50px; 
            outline: none; 
            box-sizing: border-box; 
            font-size: 16px;
            box-shadow: inset 0 0 5px rgba(0, 242, 255, 0.2);
        }
        .arc-reactor { 
            width: 60px; 
            height: 60px; 
            border: 3px double #00f2ff; 
            border-radius: 50%; 
            margin: 0 auto 10px; 
            animation: pulse 2s infinite ease-in-out; 
            background: radial-gradient(circle, rgba(0,242,255,0.1) 0%, transparent 70%);
        }
        @keyframes pulse {
            0% { transform: scale(1); box-shadow: 0 0 10px #00f2ff; }
            50% { transform: scale(1.05); box-shadow: 0 0 30px #00f2ff; }
            100% { transform: scale(1); box-shadow: 0 0 10px #00f2ff; }
        }
        .user-tag { color: #fff; margin-top: 12px; font-weight: bold; font-size: 14px; }
        .jarvis-tag { color: #00f2ff; margin-top: 8px; border-left: 2px solid #00f2ff; padding-left: 10px; font-size: 15px; }
    </style>
</head>
<body>
    <div class="main-container">
        <div class="arc-reactor"></div>
        <div style="font-size: 10px; letter-spacing: 3px; margin-bottom: 10px; text-align: center;">DEEPSEEK V3 CORE ACTIVE</div>
        <div id="display">
            <div class="jarvis-tag">SYSTEM ONLINE. STANDING BY FOR YOUR COMMANDS, SIR ARSLAN.</div>
        </div>
        <div class="input-box">
            <input type="text" id="userInput" placeholder="Listening..." onkeypress="if(event.key==='Enter') send()">
        </div>
    </div>

    <script>
        async function send() {
            let input = document.getElementById('userInput');
            let display = document.getElementById('display');
            let msg = input.value;
            if(!msg) return;

            display.innerHTML += `<div class="user-tag">ARSLAN: ${msg}</div>`;
            input.value = '';
            display.scrollTop = display.scrollHeight;
            
            try {
                let res = await fetch('/chat?msg=' + encodeURIComponent(msg));
                let data = await res.json();
                display.innerHTML += `<div class="jarvis-tag">JARVIS: ${data.reply}</div>`;
            } catch (e) {
                display.innerHTML += `<div style="color:red;">CORE DISCONNECTED. CHECK NETWORK.</div>`;
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
    url = "https://api.sambanova.ai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {SAMBA_KEY}",
        "Content-Type": "application/json"
    }
    
    # ✅ MODEL UPDATED TO DeepSeek-V3
    data = {
        "model": "DeepSeek-V3",
        "messages": [
            {"role": "system", "content": "You are JARVIS, the loyal AI assistant for Sir Arslan. Keep your responses short and professional."},
            {"role": "user", "content": msg}
        ],
        "temperature": 0.7
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=20)
        result = response.json()
        
        if 'choices' in result:
            reply = result['choices'][0]['message']['content'].strip()
        else:
            # Fallback agar DeepSeek busy ho toh Llama try karein
            reply = "Sir, DeepSeek core is busy. Should I switch to Llama 3.1 fallback?"
            
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": "Sir, internal circuits are stable but the link is unresponsive. Please check the API key on SambaNova."})
