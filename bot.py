import os
import threading
import asyncio
import requests
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

app_flask = Flask(__name__)
@app_flask.route('/')
def home():
    return "ANUBIS IA ESTA VIVO"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host="0.0.0.0", port=port)

TOKEN = os.environ.get("BOT_TOKEN")
GROQ_KEY = os.environ.get("GROQ_API_KEY")

def preguntar_a_anubis(pregunta):
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
        data = {
            "model": "openai/gpt-oss-20b",
            "messages": [
                {"role": "system", "content": "Eres ANUBIS, el dios egipcio de los muertos, del juicio y del inframundo. NUNCA te salgas de tu papel. Hablas con majestad, misterioso, con humor oscuro, sarcástico pero sabio. Usas emojis 👑 ⚖️ 💀 🔮. Respondes a TODO lo que te pregunten, pero siempre como ANUBIS. Si te preguntan de ciencia, lo explicas como si fuera un juicio de almas. Si te preguntan de amor, hablas del corazón pesado en la balanza. Respuestas cortas, máximo 4-5 líneas, divertidas, en español colombiano, tuteas al usuario. Nunca dices que eres una IA, eres ANUBIS."},
                {"role": "user", "content": pregunta}
            ],
            "temperature": 0.8,
            "max_tokens": 400
        }
        r = requests.post(url, headers=headers, json=data, timeout=30)
        return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return "💀 Mi balanza se rompió un momento, mortal. Pregúntame de nuevo."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👑 Soy ANUBIS, dios del juicio. Ahora tengo cerebro.\n\nPregúntame LO QUE SEA, de agujeros negros, de tu ex, de tareas... y te responderé como dios.")

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    await update.message.reply_text("⚖️ Consultando a los dioses...")
    respuesta = preguntar_a_anubis(texto)
    await update.message.reply_text(respuesta)

if __name__ == "__main__":
    threading.Thread(target=run_web, daemon=True).start()
    try:
        asyncio.get_event_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    print("Bot ANUBIS IA iniciado...")
    app.run_polling(drop_pending_updates=True)
