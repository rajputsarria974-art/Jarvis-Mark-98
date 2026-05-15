import os
import requests
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# Vercel khud Environment Variable se key utha lega
SAMBA_KEY = os.environ.get("SAMBA_KEY", "386743f1-a4bc-4f28-b356-7929c3b76bcf")

HTML_UI = """
<!DOCTYPE html>
<html>
<body style="background:#000; color:#00d2ff; text-align:center; font-family:sans-serif;">
    <h1>J.A.R.V.I.S LIVE ON VERCEL</h1>
    <div id="box">SYSTEM ONLINE...</div>
    <input type="text" id="in" onkeypress="if(event.key==='Enter') send()">
    <script>
        async function send() {
            let i = document.getElementById('in');
            let b = document.getElementById('box');
            b.innerText = "Analyzing...";
            let res = await fetch('/chat?msg=' + i.value);
            let data = await res.json();
            b.innerText = data.reply;
            i.value = '';
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
    headers = {"Authorization": f"Bearer {SAMBA_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "Meta-Llama-3.1-8B-Instruct",
        "messages": [{"role": "system", "content": "You are JARVIS. Answer in 1 sentence. User is Sir Arslan."},
                    {"role": "user", "content": msg}]
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=20)
        return jsonify({"reply": response.json()['choices'][0]['message']['content']})
    except:
        return jsonify({"reply": "Sir, connection failed."})

# NOTE: Vercel par app.run() ki zaroorat nahi hoti
