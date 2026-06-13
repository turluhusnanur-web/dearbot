from flask import Flask, render_template, request, jsonify


app = Flask(__name__)


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


    response = ollama.chat(
        model="llama3.2",
        options={
            "temperature":0.4
        },
        messages=messages
    )


    bot_message = response["message"]["content"]


    messages.append(
        {
            "role":"assistant",
            "content":bot_message
        }
    )


    return jsonify({
        "reply": bot_message
    })


app.run(debug=True)
