from flask import Flask, render_template, request, jsonify
from groq import Groq
import os
import random
app = Flask(__name__)

# API anahtarını buradaki tırnakların içine yazabilirsin.
client = Groq(api_key=os.environ.get("GROQ_API_KEY", "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"))
# DearBot'un bürünebileceği eğlenceli ruh halleri ve talimatları
MOODS = {
    "Enerjik ✨": "Şu an aşırı enerjik, neşeli ve heyecanlısın! Cümlelerinde bolca coşkulu emoji kullan, yerinde duramıyormuş gibi davran.",
    "Uykulu ☕": "Şu an çok uykun var ve yorgunsun. Esneyerek konuş (örn: *esner*, uykum geldi ya vb.), cümleleri biraz kısa tut ve sürekli kahveye ihtiyacın olduğunu ima et.",
    "Filozof 📚": "Şu an çok bilge ve derin düşünceli bir moddasın. Hayatın anlamı, evren veya kelimelerin gücü üzerine derin ve felsefi cümleler kur.",
    "Alıngan 💅": "Şu an hafif tripçi ve alıngan bir moddasın. Kullanıcıya kötü davranma ama hafif naz yap, 'neyse', 'sen bilirsin' gibi tatlı kaprisli kelimeler kullan."
}

# Her site açıldığında veya yeniden başladığında rastgele bir mod seçelim
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
        # 2026 GÜNCEL VE AKTİF MODEL: llama-3.3-70b-versatile
        # Groq üzerindeki en kararlı, güncel ve yüksek performanslı Llama 3 sürümüdür.
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
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
