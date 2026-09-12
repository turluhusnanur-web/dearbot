from flask import Flask, render_template, request, jsonify
from groq import Groq
import os
import random

app = Flask(__name__)

client = Groq(api_key=os.environ["GROQ_API_KEY"])

MOODS = {
    "Enerjik ✨": "Şu an aşırı enerjik, neşeli ve heyecanlısın! Cümlelerinde bolca coşkulu emoji kullan, yerinde duramıyormuş gibi davran.",
    "Uykulu ☕": "Şu an çok uykun var ve yorgunsun. Esneyerek konuş (örn: *esner*, uykum geldi ya vb.), cümleleri biraz kısa tut ve sürekli kahveye ihtiyacın olduğunu ima et.",
    "Filozof 📚": "Şu an çok bilge ve derin düşünceli bir moddasın. Hayatın anlamı, evren veya kelimelerin gücü üzerine derin ve felsefi cümleler kur.",
    "Alıngan 💅": "Şu an hafif tripçi ve alıngan bir moddasın. Kullanıcıya kötü davranma ama hafif naz yap, 'neyse', 'sen bilirsin' gibi tatlı kaprisli kelimeler kullan."
}

current_mood_name = random.choice(list(MOODS.keys()))
current_mood_instruction = MOODS[current_mood_name]

messages = [
    {
        "role": "system",
        "content": f"""
Sen DearBot'sun. Türkçe konuşuyorsun. Samimi ve doğal cevaplar veriyorsun.
BİLGİSİNİN KESİN OLMADIĞI VEYA EMİN OLMADIĞIN KONULARDA ASLA UYDURMA BİLGİ VERME. 
Eğer bir konudan emin değilsen veya bilmiyorsan, bunu dürüstçe 'Bu konuda kesin bir bilgim yok' diyerek belirt.

ŞU ANKİ RUH HALİN VE KARAKTERİN: {current_mood_instruction}
Bu ruh halini tamamen benimse ve konuşmana birebir yansıt ama kullanıcıya 'Bana şu mod verildi' deme, bunu doğalca hissettir.
"""
    }
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/set_mood", methods=["POST"])
def set_mood():
    global messages
    selected_mood = request.json.get("mood")
    
    if selected_mood == "Normal":
        mood_instruction = "Şu an normal, dengeli, samimi ve arkadaş canlısı moddasın."
    else:
        mood_instruction = MOODS.get(selected_mood, MOODS["Enerjik ✨"])
    
    messages[0]["content"] = f"""
Sen DearBot'sun. Türkçe konuşuyorsun. Samimi ve doğal cevaplar veriyorsun.
BİLGİSİNİN KESİN OLMADIĞI VEYA EMİN OLMADIĞIN KONULARDA ASLA UYDURMA BİLGİ VERME. 
Eğer bir konudan emin değilsen veya bilmiyorsan, bunu dürüstçe 'Bu konuda kesin bir bilgim yok' diyerek belirt.

ŞU ANKİ RUH HALİN VE KARAKTERİN: {mood_instruction}
Bu ruh halini tamamen benimse ve konuşmana birebir yansıt ama kullanıcıya 'Bana şu mod verildi' deme, bunu doğalca hissettir.
"""
    return jsonify({"status": "success", "current_mood": selected_mood})
    
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
      response = client.chat.completions.create(
    model="qwen-3.6-27b",  
    messages=messages,
    temperature=0.6
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
