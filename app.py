from flask import Flask, render_template, request, jsonify
from groq import Groq
import os

app = Flask(__name__)

# API anahtarını buradaki tırnakların içine yazabilirsin.
client = Groq(api_key=os.environ.get("GROQ_API_KEY", "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"))

messages = [
    {
        "role": "system",
        "content": """
Sen DearBot'sun.
Türkçe konuş.
Samimi ve doğal cevaplar ver.
"""
    }
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]

    messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    try:
        # KESİN VE AKTİF MODEL: llama3-8b-8192
        # Groq üzerinde metin sohbetleri için en hızlı ve sorunsuz çalışan ana Llama 3 modelidir.
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages,
            temperature=0.4
        )
        bot_message = response.choices[0].message.content
    except Exception as e:
        bot_message = f"Uf küçük bir bağlantı hatası aldım: {str(e)}"

    messages.append(
        {
            "role": "assistant",
            "content": bot_message
        }
    )

    return jsonify({
        "reply": bot_message
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
