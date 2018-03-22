from telegram.ext import Updater, CommandHandler
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

with open("TOKEN", 'r') as f:
    token = f.readline()
    token.strip("\n")


class Pybot:
    name = 'Pyrite'
    updater = Updater(token=token)

    dispatcher = updater.dispatcher

    def __init__(self):
        Pybot.handlers(self)
        Pybot.updater.start_polling()
        Pybot.updater.idle()

    def start(bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="Hola, prueba con /help")

    def help(bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="Jeje ni puta idea ")

    def handlers(self):
        start_handler = CommandHandler('start', Pybot.start)
        help_handler = CommandHandler('help', Pybot.help)
        Pybot.dispatcher.add_handler(start_handler)
        Pybot.dispatcher.add_handler(help_handler)



if __name__ == '__main__':

    bot = Pybot()


