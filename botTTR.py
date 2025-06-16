import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Prendi il token dalla variabile d'ambiente
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN environment variable not set.")
    exit(1) # Esci se il token non è presente

# ... il resto del tuo codice del bot ...

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Ciao! Sono il tuo bot su Render!')

def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)

def error(update: Update, context: CallbackContext) -> None:
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    dispatcher.add_error_handler(error)

    # Per il deploy, si usa generalmente il polling per i bot semplici,
    # ma i webhook sono preferibili per bot ad alto traffico o per
    # l'utilizzo di servizi serverless.
    # Per Render, il polling va bene per un worker.
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()