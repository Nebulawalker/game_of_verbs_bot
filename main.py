from loguru import logger
from environs import Env

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def main() -> None:
    env = Env()
    env.read_env()
    
    TELEGRAM_BOT_TOKEN = env.str('TELEGRAM_BOT_TOKEN')

    updater = Updater(TELEGRAM_BOT_TOKEN)
    logger.add(
        'logs/debug.log',
        format='{time:HH:mm}  {level}  {message}',
        level='DEBUG'
    )
    
    logger.info('Бот запущен!')
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    
    
    updater.idle()


if __name__ == '__main__':
    main()