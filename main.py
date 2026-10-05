import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8836458657:AAG61tpdwYu4vq5dr8ssH_KB_k658mZBi-M"

# Servidor Flask para mantener el bot activo en Render
web_app = Flask('')

@web_app.route('/')
def home():
    return "Bot activo y corriendo"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = threading.Thread(target=run_flask)
    t.start()

# Funciones del Bot de Telegram
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! Soy Kuri. ¿En qué te puedo ayudar hoy?")

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto_usuario = update.message.text
    await update.message.reply_text(f"Recibí tu mensaje: {texto_usuario}")

if __name__ == '__main__':
    keep_alive()  # Inicia el servidor web en segundo plano
    
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    
    print("Bot activo y escuchando...")
    app.run_polling()
