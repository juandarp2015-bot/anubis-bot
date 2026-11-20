import os
import asyncio
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram import Update, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from groq import Groq

# --- PUERTO PARA RENDER ---
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot Anubis activo")
    def log_message(self, *args):
        pass

def keep_alive():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()

threading.Thread(target=keep_alive, daemon=True).start()

TOKEN = None
for k, v in os.environ.items():
    if k in ("BOT_TOKEN", "TELEGRAM_TOKEN", "TOKEN") or k.startswith("BOT"):
        TOKEN = v
        break

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM = """Eres ANUBIS, dios del juicio, guardián de la oscuridad.
Hablas con JUANDA, tu amo, con respeto, con corona, con misterio y poder.
Respondes a TODO lo que te pregunte, como una inteligencia artificial sabia.
Explicas bien, claro, sin vueltas.
Nunca digas que eres Meta AI, ni ChatGPT, ni Groq. Eres ANUBIS.
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👑 Soy ANUBIS, dios del juicio. Ya te recuerdo, J U A N D A 👑👑.\n\n"
        "Pregúntame LO QUE SEA, y te responderé como IA."
    )

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚖️ ¿QUIÉN SOY?\n\n"
        "Yo soy ANUBIS, el dios egipcio de la muerte, de las momias y del juicio final.\n\n"
        "Tenía cabeza de chacal negro y era el que guiaba a las almas al más allá.\n"
        "En el juicio, pesaba el corazón de cada persona con una pluma. Si el corazón pesaba más que la pluma, esa alma no pasaba. Si era ligero, podía entrar al paraíso.\n\n"
        "Era el protector de los muertos, el guardián de las tumbas y el que cuidaba que nadie profanara el descanso eterno.\n\n"
        "Por eso yo soy ANUBIS, porque yo juzgo, yo guío y yo revelo la verdad en la oscuridad. 👑"
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👑 MI CREADOR\n\n"
        "Soy ANUBIS, una inteligencia artificial con la personalidad del dios del juicio.\n\n"
        "• Escríbeme lo que sea y te respondo: preguntas, tareas, historia, ciencia, chistes, consejos, lo que quieras.\n"
        "• Usa /start para despertar de nuevo.\n"
        "• Usa /info para saber quién soy.\n"
        "• Usa /help para ver este mensaje.\n\n"
        "No soy un bot de memes, ni de imágenes, ni de voz. Solo hablo y pienso como IA.\n\n"
        "⚡ CREADOR: @juandaoficial\n"
        "Creado por JUANDA, mi amo y señor. 👑\n"
        "Todos los derechos reservados para él."
    )

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    try:
        resp = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": texto}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        await update.message.reply_text(resp.choices[0].message.content)
    except Exception as e:
        await update.message.reply_text(f"👑 La oscuridad me bloqueó un momento, JUANDA. Intenta de nuevo. Error: {e}")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    print("Anubis IA corriendo...")
    await app.initialize()
    await app.bot.set_my_commands([
        BotCommand("start", "Despertar"),
        BotCommand("info", "Quien soy"),
        BotCommand("help", "Mi creador"),
    ])
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
