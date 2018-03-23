from telegram.ext import MessageHandler,CommandHandler,Filters,Updater
import logging, random, re
from praw import Reddit


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

with open("config", 'r') as f:
    token = f.readline().strip("\n")
    user_id = f.readline().strip("\n")


with open("redditauth",'r') as f:
    reddit_secret = f.readline().strip("\n")
    reddit_pass = f.readline().strip("\n")
    reddit_user = f.readline().strip("\n")


class Pybot:
    name = 'Pyrite'
    updater = Updater(token=token)
    var = updater.bot.get_updates
    dispatcher = updater.dispatcher
    boobarray = []


    def __init__(self, name):
        Pybot.handlers(self)
        Pybot.updater.start_polling()
        Pybot.updater.idle()
        Pybot.name = name
        print(Pybot.auth_reddit.user.me())

    def reddit(self):
        auth_reddit = Reddit(client_id='oy5ifWn5vvoDOg',
                             client_secret=reddit_secret,
                             password=reddit_pass,
                             user_agent='pyrite',
                             username=reddit_user)
        multiboobs = auth_reddit.multireddit('Endirable', 'boobs')
        genboob = multiboobs.hot()
        for submission in genboob:
            # Check for all the cases where we will skip a submission:
            if "imgur.com/" in submission.url:
                Pybot.boobarray.append(submission.url)

    #Commands
    def start(bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="[{0}]:  Hola, prueba con /help".format(Pybot.name))
        print(update.message.chat_id)

    def help(bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="Jeje ni puta idea ")

    def torrent(bot, update):
        superid = update.message.chat_id
        if str(superid) == str(user_id):
            bot.send_message(chat_id=update.message.chat_id, text="Hola Mario!")
        else:
            bot.send_message(chat_id=update.message.chat_id, text="Si fueras Mario hasta te dejaba y todo")

    def tetas(bot, update):
        print(len(Pybot.boobarray))
        if len(Pybot.boobarray) > 0:
            bot.send_photo(chat_id=update.message.chat_id, photo=Pybot.boobarray.pop())
        else:
            Pybot.reddit(Pybot)
            bot.send_message(chat_id=update.message.chat_id, text="Estoy buscando pezones como Magdalenas... usa el comando otra vez")


    #Messages
    def echo(bot, update):
        message, randomized = '', ''
        re.sub("[aAoOuU]", str(update.message.text),message)


        #For each char in the message, capitalize randomly (7 10)
        for num in message:
            ran = random.randint(0,10)
            if(ran >= 7):
                if num == 'i':
                    randomized = randomized + num
                    continue
                randomized = randomized + num.capitalize()

            else:
                randomized = randomized + num.lower()

        bot.send_message(chat_id=update.message.chat_id, text=randomized)

        #Save new_member id and name in a plain text
    def new_member(bot, update):
        new_member = update.message.new_chat_members
        lil = '{0}'.format(new_member[0])
        with open('user_info', 'w') as entrada:
            entrada.write(lil + "\n" )


    def handlers(self):
        start_handler = CommandHandler('start', Pybot.start)
        help_handler = CommandHandler('help', Pybot.help)
        torrent_handler = CommandHandler('torrent', Pybot.torrent)
        echo_handler = MessageHandler(Filters.text, Pybot.echo)
        users_group_handler = MessageHandler(Filters.status_update.new_chat_members, Pybot.new_member)
        tetas_handler = CommandHandler('tetas', Pybot.tetas)

        Pybot.dispatcher.add_handler(start_handler)
        Pybot.dispatcher.add_handler(help_handler)
        Pybot.dispatcher.add_handler(echo_handler)
        Pybot.dispatcher.add_handler(torrent_handler)
        Pybot.dispatcher.add_handler(users_group_handler)
        Pybot.dispatcher.add_handler(tetas_handler)



if __name__ == '__main__':

    bot = Pybot('Running')



