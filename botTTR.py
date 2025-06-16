import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- Configurazione Iniziale ---

# Configura il logging per visualizzare gli eventi nel terminale
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)

# Recupera il token del bot dalla variabile d'ambiente
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    logger.error(
        "ERRORE: La variabile d'ambiente 'TELEGRAM_BOT_TOKEN' non è impostata."
    )
    logger.error(
        "Assicurati di aver configurato il token del bot nel tuo ambiente di deploy."
    )
    exit(1)

# --- Funzioni di Gestione dei Comandi e Messaggi ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Gestisce il comando /start."""
    user = update.effective_user
    logger.info(f"Comando /start ricevuto da {user.full_name} (ID: {user.id})")
    await update.message.reply_html(
        rf"Ciao {user.mention_html()}! Sono un bot d'esempio. Puoi scrivermi qualcosa e io ti risponderò, oppure prova i comandi: /info",
    )

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Gestisce il comando /info."""
    user = update.effective_user
    chat_id = update.effective_chat.id
    logger.info(
        f"Comando /info ricevuto da {user.full_name} nella chat {chat_id}")

    info_text = (
        "Ecco alcune informazioni di base su Telegram:\n\n"
        "🌐 Telegram è un'applicazione di messaggistica istantanea basata su cloud e crittografata.\n"
        "👥 Permette di creare chat private, gruppi (fino a 200.000 membri) e canali (per broadcast a un pubblico illimitato).\n"
        "🤖 I bot sono programmi di terze parti che girano su Telegram e possono fare molte cose, da semplici giochi a strumenti complessi.\n"
        "🔒 Offre chat segrete con crittografia end-to-end e autodistruzione dei messaggi.\n"
        "☁️ Tutti i dati sono archiviati nel cloud, permettendo l'accesso da qualsiasi dispositivo.\n\n"
        "Spero ti sia utile!")
    await update.message.reply_text(info_text)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Risponde al messaggio di testo dell'utente con lo stesso testo (funzione eco)."""
    logger.info(
        f"Messaggio ricevuto: '{update.message.text}' da {update.effective_user.full_name}"
    )
    await update.message.reply_text(update.message.text)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Logga gli errori causati dagli aggiornamenti."""
    logger.warning(f'Update "{update}" ha causato errore "{context.error}"')

# --- Funzione Principale per l'Avvio del Bot ---

def main():
    """Avvia il bot."""
    # Crea l'Application
    application = Application.builder().token(TOKEN).build()

    # Registra i gestori dei comandi
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("info", info))

    # Registra il gestore per i messaggi di testo (che non sono comandi)
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Registra il gestore degli errori
    application.add_error_handler(error_handler)

    # Avvia il bot usando il polling
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()