import os, threading, asyncio, requests, random, re, urllib.parse
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

nombres = {}

def preguntar_a_anubis(pregunta, nombre="mortal"):
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
        data = {
            "model": "openai/gpt-oss-20b",
            "messages": [
                {"role": "system", "content": f"Eres ANUBIS, dios egipcio. Hablas con majestad, humor oscuro, sarcástico, sabio. Usas emojis 👑 ⚖️ 💀 🔮. El usuario se llama {nombre}, llámalo por su nombre a veces. Respuestas cortas, máximo 3-4 líneas, español colombiano, tuteas. Nunca dices que eres IA, eres ANUBIS."},
                {"role": "user", "content": pregunta}
            ],
            "temperature": 0.8,
            "max_tokens": 300
        }
        r = requests.post(url, headers=headers, json=data, timeout=30)
        return r.json()["choices"][0]["message"]["content"]
    except:
        return "Mi balanza se rompió un momento, mortal. Pregúntame de nuevo."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombre = update.effective_user.first_name
    nombres[update.effective_user.id] = nombre
    await update.message.reply_text(f"👑 Soy ANUBIS, dios del juicio. Ya te recuerdo, {nombre}.\n\nPregúntame LO QUE SEA.\n\nComandos:\n🎭 /meme\n🎨 /imagen un gato egipcio\n🔊 /voz hola como estas")

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    nombre = nombres.get(user_id, update.effective_user.first_name)
    nombres[user_id] = nombre
    texto = update.message.text
    await update.message.reply_text("⚖️ Consultando a los dioses...")
    respuesta = preguntar_a_anubis(texto, nombre)
    await update.message.reply_text(respuesta)

async def meme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎭 Buscando meme en el inframundo...")
    try:
        r = requests.get("https://meme-api.com/gimme", timeout=15).json()
        await update.message.reply_photo(photo=r["url"], caption="💀 Meme juzgado por ANUBIS 👑")
    except:
        await update.message.reply_text("💀 No encontré memes, mortal.")

async def imagen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args)
    if not prompt:
        await update.message.reply_text("🎨 Escribe: /imagen un gato faraón")
        return
    await update.message.reply_text(f"🎨 Pintando: {prompt}...")
    url = f"https://image.pollinations.ai/prompt/{prompt} egyptian god style?width=512&height=512&seed={random.randint(1,9999)}"
    await update.message.reply_photo(photo=url, caption=f"👑 Creado por ANUBIS: {prompt}")

async def voz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = " ".join(context.args)
    if not texto:
        await update.message.reply_text("🔊 Escribe: /voz hola mortal")
        return
    await update.message.reply_text("🔊 ANUBIS está hablando...")
    respuesta = preguntar_a_anubis(texto, nombres.get(update.effective_user.id, "mortal"))
    await update.message.reply_text(respuesta)
    try:
        limpio = re.sub(r'[^\w\s.,!?¿¡áéíóúÁÉÍÓÚñÑ-]', '', respuesta)
        limpio = limpio.replace('\n', ' ')[:400]
        if not limpio.strip():
            limpio = "Hola mortal, soy Anubis"
        
        texto_url = urllib.parse.quote(limpio)
        url_voz = f"https://api.streamelements.com/kappa/v2/speech?voice=Enrique&text={texto_url}"
        r = requests.get(url_voz, timeout=20)
        with open("/tmp/anubis.mp3", "wb") as f:
            f.write(r.content)
        # CORREGIDO: como AUDIO, no como VOICE, para que muestre duración
        with open("/tmp/anubis.mp3", "rb") as f:
            await update.message.reply_audio(audio=f, filename="anubis.mp3", title="ANUBIS HABLA")
    except Exception as e:
        await update.message.reply_text(f"💀 No pude hablar: {e}")

if __name__ == "__main__":
    threading.Thread(target=run_web, daemon=True).start()
    try:
        asyncio.get_event_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("meme", meme))
    app.add_handler(CommandHandler("imagen", imagen))
    app.add_handler(CommandHandler("voz", voz))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    print("Bot ANUBIS IA iniciado...")
    app.run_polling(drop_pending_updates=True)
