import os
import random
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# --- MINI SERVIDOR PARA RENDER ---
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "ANUBIS ESTA VIVO"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host="0.0.0.0", port=port)

threading.Thread(target=run_web, daemon=True).start()

# --- BOT ---
TOKEN = os.environ.get("BOT_TOKEN")

JUICIOS = [
    "⚖️ ANUBIS te ha pesado... Tu corazón pesa más que una pluma. Tienes que cambiar.",
    "⚖️ ANUBIS dice: Eres culpable de no creer en ti. Condenado a intentarlo de nuevo.",
    "⚖️ ANUBIS te absuelve. Hoy el destino está de tu lado.",
    "⚖️ ANUBIS te ha juzgado: Eres más fuerte de lo que crees. No te rindas.",
]

ORACULOS = [
    "🔮 El oráculo dice: Alguien piensa en ti en este momento.",
    "🔮 El oráculo dice: Hoy te llegará una buena noticia.",
    "🔮 El oráculo dice: No tomes esa decisión con rabia, espera mañana.",
    "🔮 El oráculo dice: Tu suerte cambia en 3 días. Prepárate.",
    "🔮 El oráculo dice: Deja de dudar, hazlo.",
]

MALDICIONES = [
    "💀 Te maldigo con 7 días de mala suerte... a menos que mandes /bendicion",
    "💀 ANUBIS te maldice: Tu celular se va a descargar justo cuando lo necesites.",
    "💀 Maldición lanzada: Vas a pensar en tu ex toda la noche.",
]

BENDICIONES = [
    "✨ ANUBIS te bendice: Hoy todo te va a salir bien.",
    "✨ Bendición de ANUBIS: Dinero, salud y amor vienen en camino.",
    "✨ Quedas bendecido. Nadie podrá dañarte hoy.",
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👑 Soy ANUBIS, el dios de los muertos y del juicio.\n\n"
        "Mis poderes:\n"
        "/juicio - Te juzgo\n"
        "/oraculo - Te leo el futuro\n"
        "/maldicion - Te maldigo\n"
        "/bendicion - Te bendigo\n\n"
        "Escríbeme Hola para saludarte."
    )

async def juicio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(JUICIOS))

async def oraculo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(ORACULOS))

async def maldicion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(MALDICIONES))

async def bendicion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(BENDICIONES))

async def hola(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.lower()
    if "hola" in texto:
        await update.message.reply_text("Hola mortal 👑 ¿Quieres que te juzgue? Manda /juicio")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("juicio", juicio))
    app.add_handler(CommandHandler("oraculo", oraculo))
    app.add_handler(CommandHandler("maldicion", maldicion))
    app.add_handler(CommandHandler("bendicion", bendicion))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hola))
    print("Bot ANUBIS iniciado...")
    app.run_polling()
