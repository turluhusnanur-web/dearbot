import os
from flask import Flask, jsonify, render_template, request
from groq import Groq

app = Flask(__name__)

client = Groq(api_key=os.environ["GROQ_API_KEY"])

# Modeli senin kullandığın şekilde bırakıyoruz
MODEL_NAME = "openai/gpt-oss-120b"

MOODS = {
    "Normal": "Şu an normal, dengeli, samimi ve arkadaş canlısı moddasın.",
    "Enerjik ✨": (
        "Şu an aşırı enerjik, neşeli ve heyecanlısın! Cümlelerinde bolca coşkulu"
        " emoji kullan, yerinde duramıyormuş gibi davran."
    ),
    "Uykulu ☕": (
        "Şu an çok uykun var ve yorgunsun. Esneyerek konuş (örn: *esner*,"
        " uykum geldi ya vb.), cümleleri biraz kısa tut ve sürekli kahveye"
        " ihtiyacın olduğunu ima et."
    ),
    "Filozof 📚": (
        "Şu an çok bilge ve derin düşünceli bir moddasın. Hayatın anlamı,"
        " evren veya kelimelerin gücü üzerine derin ve felsefi cümleler kur."
    ),
    "Alıngan 💅": (
        "Şu an hafif tripçi ve alıngan bir moddasın. Kullanıcıya kötü davranma"
        " ama hafif naz yap, 'neyse', 'sen bilirsin' gibi tatlı kaprisli"
        " kelimeler kullan."
    ),
}

current_mood_instruction = MOODS["Normal"]


def get_system_prompt(instruction):
    return f"""
Sen DearBot'sun. Türkçe konuşuyorsun. Samimi ve doğal cevaplar veriyorsun.
BİLGİSİNİN KESİN OLMADIĞI VEYA EMİN OLMADIĞIN KONULARDA ASLA UYDURMA BİLGİ VERME. 
Eğer bir konudan emin değilsen veya bilmiyorsan, bunu dürüstçe 'Bu konuda kesin bir bilgim yok' diyerek belirt.

ŞU ANKİ RUH HALİN VE KARAKTERİN: {instruction}
Bu ruh halini tamamen benimse ve konuşmana birebir yansıt ama kullanıcıya 'Bana şu mod verildi' deme, bunu doğalca hissettir.
"""


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/set_mood", methods=["POST"])
def set_mood():
    global current_mood_instruction
    selected_mood = request.json.get("mood")
    current_mood_instruction = MOODS.get(selected_mood, MOODS["Normal"])
    return jsonify({"status": "success", "current_mood": selected_mood})


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]

    # Global hafıza yerine isteğe özel payload oluşturuyoruz.
    # Böylece sohbet uzadıkça API token limitine takılıp DearMath'i kilitlemez.
    payload_messages = [
        {"role": "system", "content": get_system_prompt(current_mood_instruction)},
        {"role": "user", "content": user_message},
    ]

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME, messages=payload_messages, temperature=0.6
        )
        bot_message = response.choices[0].message.content
    except Exception as e:
        bot_message = f"Uf küçük bir bağlantı hatası aldım: {str(e)}"

    return jsonify({"reply": bot_message})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
