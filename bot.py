from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import re
import random

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

    def echo(bot, update):
        mens = str(update.message.text)
        ii = re.sub("[aAoOuU]", "i", mens)
        stri = ''
        for num in ii:
            ran = random.randint(0,1)
            if(ran == 1):
                if(num == 'i'):
                    stri = stri + num
                    continue
                stri = stri + num.capitalize()

            else:
                stri = stri + num.lower()
        print(str(ii))
        bot.send_message(chat_id=update.message.chat_id, text=stri)

    def handlers(self):
        start_handler = CommandHandler('start', Pybot.start)
        help_handler = CommandHandler('help', Pybot.help)
        echo_handler = MessageHandler(Filters.text, Pybot.echo)
        Pybot.dispatcher.add_handler(start_handler)
        Pybot.dispatcher.add_handler(help_handler)
        Pybot.dispatcher.add_handler(echo_handler)



if __name__ == '__main__':

    bot = Pybot()


