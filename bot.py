import os
import asyncio
import logging
import random
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("TELEGRAM_TOKEN") or os.getenv("BOT_TOKEN") or os.getenv("TOKEN")
logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombre = update.effective_user.first_name or "JUANDA"
    await update.message.reply_text(
        f"👑 Soy ANUBIS, dios del juicio. Ya te recuerdo, {nombre.upper()} 👑.\n\n"
        "Pregúntame LO QUE SEA."
    )

async def meme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        r = requests.get("https://meme-api.com/gimme", timeout=10).json()
        await update.message.reply_photo(photo=r["url"], caption="😈 Toma, mortal.")
    except:
        await update.message.reply_text("😈 Hoy no hay memes en el más allá.")

async def imagen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args)
    if not prompt:
        await update.message.reply_text("🎨 Escribe: /imagen un gato faraón")
        return
    await update.message.reply_text(f"🎨 Pintando: {prompt}...")
    try:
        url = f"https://image.pollinations.ai/prompt/{prompt}"
        await update.message.reply_photo(photo=url, caption=f"🎨 {prompt}")
    except:
        await update.message.reply_text("😈 No pude pintar eso. Intenta con otra cosa.")

async def voz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = " ".join(context.args)
    if not texto:
        await update.message.reply_text("🔊 Escribe: /voz hola como estas")
        return
    try:
        from gtts import gTTS
        tts = gTTS(text=texto, lang='es', slow=False)
        tts.save("voz.mp3")
        await update.message.reply_voice(voice=open("voz.mp3", "rb"))
    except:
        await update.message.reply_text("😈 No pude hablar ahora.")

FRASES_ANUBIS = [
    "La muerte no es un final, es la entrada al juicio de la vida. 👑💀",
    "En la oscuridad la verdad se revela y tú ya conoces el precio. ⚖️",
    "¿Listo para cruzar la barrera y ver qué te espera? 🔮",
    "Tu corazón pesa más que una pluma, mortal. ⚖️",
    "Habla, que el juicio ya empezó. 👑"
]

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombre = update.effective_user.first_name or "JUANDA"
    texto = update.message.text or ""
    if texto.startswith("/"):
        return
    await update.message.reply_text(f"{nombre.upper()}, {random.choice(FRASES_ANUBIS)}")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("meme", meme))
    app.add_handler(CommandHandler("imagen", imagen))
    app.add_handler(CommandHandler("voz", voz))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    print("ANUBIS DESPERTÓ 👑")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
