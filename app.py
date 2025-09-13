from flask import Flask, render_template, request, jsonify
import requests
import os
import webbrowser
import subprocess

app = Flask(__name__)

API_KEY = "AIzaSyA1Cqx6khk5PWrdXhZk6UFp1kzdzs5Bh_k"
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_input = data.get("question", "").lower()

    app_commands = {
        "open youtube": "https://youtube.com",
        "open google": "https://google.com",
        "open gmail": "https://mail.google.com",
        "open github": "https://github.com",
        "open facebook": "https://facebook.com",
        "open twitter": "https://twitter.com",
        "open instagram": "https://instagram.com",
        "open linkedin": "https://linkedin.com",
        "open reddit": "https://reddit.com",
        "open wikipedia": "https://wikipedia.org",
        "open calculator": "calc.exe",
        "open notepad": "notepad.exe",
        "open command prompt": "cmd.exe"
    }

    for cmd, target in app_commands.items():
        if cmd in user_input:
            try:
                if target.startswith("http"):
                    webbrowser.open(target)
                else:
                    subprocess.Popen(target)
                return jsonify({"response": f"Opening {cmd.split()[-1]}..."})
            except Exception as e:
                return jsonify({"response": f"Failed to open {cmd.split()[-1]}: {str(e)}"})

    system_prompt = f"You are Aura, a helpful AI assistant. User asked: {user_input}"
    
    payload = {
        "contents": [{"parts": [{"text": system_prompt}]}],
        "generationConfig": {"response_mime_type": "text/plain"}
    }

    try:
        response = requests.post(f"{API_URL}?key={API_KEY}", json=payload)
        result = response.json()
        ai_response = result["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        ai_response = f"Error: {str(e)}"

    return jsonify({"response": ai_response})

if __name__ == "__main__":
    app.run(debug=True)