from flask import Flask, render_template, request, jsonify
from groq import Groq
import os

app = Flask(__name__)

# Groq API bağlantısı. API anahtarını aşağıdaki tırnakların içine güvenle yazabilirsin.
# Render'da Environment Variable ayarladıysan onu okur, ayarlamadıysan tırnak içindeki anahtarı kullanır.
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
        # Yapay zeka yanıtını internet üzerinden Groq sunucularından ışık hızında çekiyoruz
        response = client.chat.completions.create(
            model="llama-3.2-3b",
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
    # Hem kendi bilgisayarında (5000 portunda) hem de Render'da sorunsuz çalışmasını sağlayan altın ayar
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
