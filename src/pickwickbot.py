#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler
from telegram.error import InvalidToken
import logging
from questions import random_question

# Enable logging.
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Initialise variable that stores the DB connection.
conn = None


def start(bot, update):
    bot_name = bot.get_me().first_name
    update.message.reply_text('Hoi, ik ben %s!' % bot_name)


def question(_, update):
    update.message.reply_text(random_question())


def error(_, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def main(token):
    # Create the event handler and pass it your bot's token.
    try:
        updater = Updater(token)
    except InvalidToken:
        exit('Bot token is invalid.')

    bot = updater.bot

    # Get the dispatcher to register handlers.
    dp = updater.dispatcher

    # Answer the commands.
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('vraag', question))

    # Register all errors.
    dp.add_error_handler(error)

    # Start the bot.
    updater.start_polling()

    # Notify that the bot is running.
    me = bot.get_me()
    print('Your bot named %s is now running, start a conversation: '
          'https://telegram.me/%s' % (me.first_name, me.username))

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    # Ask for a bot token.
    token = input('Bot token: ')
    print('')

    # Call the main function.
    main(token)
