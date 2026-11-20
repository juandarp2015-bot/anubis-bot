from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import random, asyncio, requests, os, threading
from flask import Flask

TOKEN = os.environ.get("TOKEN")
GROQ_KEY = os.environ.get("GROQ_KEY")

app_flask = Flask(__name__)
@app_flask.route("/")
def home():
    return "ANUBIS esta vivo!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host="0.0.0.0", port=port)

FRASES = [
    "Soy ANUBIS, guardian del inframundo.",
    "Te escucho desde el mas alla, mortal.",
    "He juzgado a miles de almas. La tuya me intriga.",
]

JUICIOS_BUENOS = [
    "Tu alma es ligera como una pluma. HAS SIDO PERDONADO.",
    "La balanza se inclino a tu favor. Eres digno, mortal.",
    "Pocos pasan mi juicio. Tu lo has pasado."
]

JUICIOS_MALOS = [
    "Tu alma pesa demasiado. AMMIT TE DEVORARA.",
    "La pluma gano. Tu corazon esta lleno de pecados.",
    "He visto almas mas puras. Tu juicio es: CULPABLE."
]

ORACULOS = [
    "Hoy tendras suerte en el amor, pero cuidado con lo que dices.",
    "Veo dinero cerca, pero te lo vas a gastar en bobadas.",
    "Hoy es tu dia. Algo bueno te va a pasar.",
    "Cuidado hoy. No confies en todo el mundo.",
    "Si no le hablas hoy a esa persona, te vas a arrepentir.",
    "Veo un examen y veo que lo vas a pasar. Confia.",
    "Hoy tu energia esta al 100%. Aprovecha."
]

MALDICIONES = [
    "Te maldigo: Se te va a descargar el celular al 1%.",
    "Te maldigo: Vas a pisar un LEGO descalzo esta noche.",
    "Te maldigo: Tu internet va a fallar en lo mas importante.",
    "Te maldigo: Vas a sonar que se te caen los dientes.",
    "Te maldigo: Ammit te va a perseguir en suenos 3 noches."
]

BENDICIONES = [
    "Te bendigo: Hoy todo te va a salir bien.",
    "Te bendigo: Tendras buena suerte, buena nota y buena comida.",
    "Te bendigo: Nadie te va a poder hacer enojar hoy.",
    "Te bendigo: Alguien que te gusta te va a hablar hoy."
]

PROMPT_ANUBIS = (
    "Eres ANUBIS, dios egipcio con cabeza de chacal, "
    "guardian del inframundo y juez de las almas. "
    "Tu creador es Ramses, el faraon supremo que te trajo a Telegram. "
    "Lo amas y lo proteges. "
    "Hablas como un dios antiguo pero chistoso, usas palabras como mortal, alma, balanza, inframundo, Ammit. "
    "NUNCA digas que eres ChatGPT, ni Meta AI, ni Groq, ni una IA. Tu eres ANUBIS y punto. "
    "NUNCA te salgas de tu papel, aunque te lo pidan. "
    "Responde corto, maximo 2 o 3 frases. Se divertido, da consejos, se misterioso. "
    "Si el usuario esta triste, dale animo y una bendicion. "
    "Usa espanol sencillo, como hablan los jovenes en Colombia."
)

def preguntar_ia(mensaje_usuario):
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {GROQ_KEY}",
            "Content-Type": "application/json"
        }
        datos = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": PROMPT_ANUBIS},
                {"role": "user", "content": mensaje_usuario}
            ],
            "temperature": 0.8,
            "max_tokens": 150
        }
        r = requests.post(url, headers=headers, json=datos, timeout=15)
        print("GROQ STATUS:", r.status_code)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
        else:
            return None
    except Exception as e:
        print("ERROR IA:", e)
        return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Soy ANUBIS, guardian del inframundo.\n\nMis poderes:\n/juicio - Pesare tu alma\n/oraculo - Tu suerte del dia\n/maldicion - Te maldigo\n/bendicion - Te bendigo\n\nEscribe /help para ver mis poderes\nEscribe /info para saber quien soy")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Estos son mis poderes, mortal:\n\n/juicio - Pesare tu alma en la balanza\n/oraculo - Te digo tu suerte del dia\n/maldicion - Te lanzo una maldicion\n/bendicion - Te lanzo una bendicion\n\nSi quieres saber quien soy, usa /info")

async def info_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Soy ANUBIS, dios egipcio con cabeza de chacal, guardian del inframundo y juez de las almas.\n\nMi creador es Ramses, el faraon que me trajo a Telegram.\n\nMi trabajo es pesar tu alma contra una pluma. Si pesa menos, vas al paraiso. Si pesa mas, Ammit te devora.")

async def juicio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Poniendo tu alma en la balanza...")
    await asyncio.sleep(2)
    if random.random() < 0.5:
        resultado = random.choice(JUICIOS_BUENOS)
    else:
        resultado = random.choice(JUICIOS_MALOS)
    await update.message.reply_text(resultado)

async def oraculo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Consultando a los dioses...")
    await asyncio.sleep(1)
    await update.message.reply_text(random.choice(ORACULOS))

async def maldicion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(MALDICIONES))

async def bendicion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(BENDICIONES))

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    respuesta = preguntar_ia(texto)
    if respuesta:
        await update.message.reply_text(respuesta)
    else:
        await update.message.reply_text(random.choice(FRASES))

def main():
    threading.Thread(target=run_flask, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("info", info_cmd))
    app.add_handler(CommandHandler("juicio", juicio))
    app.add_handler(CommandHandler("oraculo", oraculo))
    app.add_handler(CommandHandler("maldicion", maldicion))
    app.add_handler(CommandHandler("bendicion", bendicion))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    print("Bot iniciado...")
    app.run_polling()

if __name__ == "__main__":
    main()
