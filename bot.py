from telegram.ext import MessageHandler, CommandHandler, Filters, Updater
from telegram import error
import logging, random, re
from praw import Reddit
from urllib.parse import urlsplit

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

with open("config", 'r') as f:
    token = f.readline().strip("\n")
    user_id = f.readline().strip("\n")

with open("redditauth", 'r') as f:
    reddit_secret = f.readline().strip("\n")
    reddit_pass = f.readline().strip("\n")
    reddit_user = f.readline().strip("\n")


class Pybot:
    name = 'Pyrite'
    updater = Updater(token=token)
    var = updater.bot.get_updates
    dispatcher = updater.dispatcher
    arrays = {"gatos": [], "tetas": [], "culos": [], "memes": []}

    def __init__(self, name):
        Pybot.handlers(self)
        Pybot.updater.start_polling()
        Pybot.updater.idle()
        Pybot.name = name

    # Fetch method to populate an array with photo strings, you have to add multirredit here
    def fetch_reddit(busqueda):
        if len(Pybot.arrays[busqueda]) is 0:
            auth_reddit = Reddit(client_id='oy5ifWn5vvoDOg',
                                 client_secret=reddit_secret,
                                 password=reddit_pass,
                                 user_agent='pyrite',
                                 username=reddit_user)
            mreddit = {"tetas": auth_reddit.multireddit('Endirable', 'boobs'),
                       "gatos": auth_reddit.multireddit('Endirable', 'cats'),
                       "culos": auth_reddit.multireddit('Endirable', 'booty'),
                       "meme": auth_reddit.multireddit('Endirable', 'memes')}
            
            postdata = mreddit[busqueda].hot()
            for submission in postdata:
                Pybot.arrays[busqueda].append(submission.url)
        print(Pybot.arrays[busqueda])



    def send_content(bot, command, ch_id):
        search = str(command)
        cn = Pybot.arrays[search].pop(0)


        try:
            if "v.redd.it/" in cn:
                cn = cn + "/DASH_1_2_M"
                bot.send_video(chat_id=ch_id, video=cn)
            if "gfycat.com/" in cn:
                splitted = urlsplit(cn)
                path = splitted.path

                parsed = "https://thumbs.gfycat.com" + path + "-size_restricted.gif"
                bot.send_video(chat_id=ch_id, video=parsed)
            elif ".gif" or ".gifv" in cn:
                bot.send_video(chat_id=ch_id, video=cn)
            elif "imgur.com/" or ".jpg" or ".jpeg" or "i.redd.it" in cn:
                bot.send_photo(chat_id=ch_id, photo=cn)

        except error.BadRequest:
            Pybot.send_content(bot, command, ch_id)
            logging.log(msg="Error enviando contenido, {0} {1} {2}".format(command,ch_id,str(error.BadRequest)), level=logging.INFO)

        except error.TimedOut:
            bot.send_message(chat_id=ch_id, text="Whoops... perdón por la espera, algo no va bien")






    # Command method to fetch images and send them to group
    def gatos(bot, update):
        Pybot.fetch_reddit('gatos')
        Pybot.send_content(bot, 'gatos', update.message.chat_id)

    def tetas(bot, update):
        Pybot.fetch_reddit('tetas')
        Pybot.send_content(bot, 'tetas', update.message.chat_id)

    def culos(bot, update):
        Pybot.fetch_reddit('culos')
        Pybot.send_content(bot, 'culos', update.message.chat_id)

    def meme(bot, update):
        Pybot.fetch_reddit('memes')
        Pybot.send_content(bot, 'memes', update.message.chat_id)

    # Commands
    def start(bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="Hola, soy {0} y sé un poco sobre \n".format(Pybot.name) +
                                                              "/torrent - Búsqueda de magnets en TPB \n" +
                                                              "/tetas - Más cómodo que Reddit (!) \n" +
                                                              "/gatos - MUCHO más cómodo que Reddit (!!)\n" +
                                                              "/facha - Para esos moments aleatorio de fascismo \n" +
                                                              "/about - Sobre {0}".format(Pybot.name))

    def about(bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="Python 3.6 - github.com/elbaridne/Pyrite")

    def torrent(bot, update):
        superid = update.message.chat_id
        if str(superid) == str(user_id):
            bot.send_message(chat_id=update.message.chat_id, text="Not yet")
        else:
            bot.send_message(chat_id=update.message.chat_id, text="Not yet")

    def facha(bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="*Faaaaaaacha*")
        bot.send_photo(chat_id=update.message.chat_id,
                       photo="https://gaceta.es/wp-content/uploads/2017/07/franco_1937.jpg")

    # Messages
    def echo(bot, update):

        input_message = update.message.text
        randomized = ''
        # For each char in the message, capitalize randomly (7 10)
        for num in input_message:
            ran = random.randint(0, 10)
            print(ran)
            if (ran >= 4):
                if num == 'i':
                    randomized = randomized + num
                    continue
                randomized = randomized + num.capitalize()

            else:
                randomized = randomized + num.lower()

        bot.send_message(chat_id=update.message.chat_id, text=randomized)

    # Save new_member id and name in a plain text

    def new_member(bot, update):
        new_member = update.message.new_chat_members
        lil = '{0}'.format(str(new_member))
        with open('user_info', 'w') as entrada:
            entrada.write(lil + "\n")

    def handlers(self):

        # Command Handlers
        start_handler = CommandHandler('start', Pybot.start)
        about_handler = CommandHandler('about', Pybot.about)
        torrent_handler = CommandHandler('torrent', Pybot.torrent)
        facha_handler = CommandHandler('facha', Pybot.facha)
        meme_handler = CommandHandler('meme', Pybot.meme)

        # Reddit Handlers busqueda = subrredit to fetch. you need an entry on the dictionary {arrays}
        #                            and the multireddit added inside {mreddit}
        tetas_handler = CommandHandler('tetas', Pybot.tetas)
        gatos_handler = CommandHandler('gatos', Pybot.gatos)
        culo_handler = CommandHandler('culos', Pybot.culos)

        # Mensage Listeners

        echo_handler = MessageHandler(Filters.text, Pybot.echo)
        users_group_handler = MessageHandler(Filters.status_update.new_chat_members, Pybot.new_member)

        # Adding handlers to dispatcher
        Pybot.dispatcher.add_handler(start_handler)
        Pybot.dispatcher.add_handler(about_handler)
        Pybot.dispatcher.add_handler(torrent_handler)
        Pybot.dispatcher.add_handler(meme_handler)
        Pybot.dispatcher.add_handler(culo_handler)
        Pybot.dispatcher.add_handler(gatos_handler)
        Pybot.dispatcher.add_handler(tetas_handler)
        Pybot.dispatcher.add_handler(facha_handler)
        Pybot.dispatcher.add_handler(users_group_handler)
        Pybot.dispatcher.add_handler(echo_handler)


if __name__ == '__main__':
    bot = Pybot('Pyrite')
