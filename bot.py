from telegram.ext import MessageHandler, CommandHandler, Filters, Updater
from telegram import error
import logging, random, re, os, sys
from praw import Reddit
from urllib.parse import urlsplit
import meme_gen

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)


class Pybot:
    name = 'Pyrite'
    try:
        with open("config", 'r') as f:
            api_tele = f.readline().strip("\n")
            tele_id = f.readline().strip("\n")
    except IOError:
        logging.log(logging.CRITICAL, "./config file missing parameters")

    updater = Updater(api_tele)
    dispatcher = updater.dispatcher
    telegram_id = tele_id
    map_r_mr = dict()
    arrays = {'': []}

    def __init__(self, name):
        dirs = (os.listdir(os.getcwd()))

        if "redditauth" in dirs:
            with open("redditauth", 'r') as f:
                reddit = dict()
                try:
                    reddit["secret"] = f.readline().strip("\n").lstrip("secret ")
                    reddit["pass"] = f.readline().strip("\n")[14:]
                    reddit["user"] = f.readline().strip("\n")[9:]
                    print(reddit)
                except Exception:
                    logging.log(logging.WARNING, "redditauth bad configuration")
                    sys.exit

            auth_reddit = Reddit(client_id='oy5ifWn5vvoDOg', client_secret=reddit["secret"],
                                 password=reddit["pass"], username=reddit["user"],
                                 user_agent='pyrite', )
            
        else:
            raise FileNotFoundError("redditauth missing")

        self.name = name

        if "multis" in dirs:
            with open("multis", 'r') as f:
                multi = f.readlines()

            for ele in multi:
                ele = ele.strip("\n")

                Pybot.map_r_mr[ele] = auth_reddit.multireddit(reddit["user"], ele)
                Pybot.arrays[ele] = []
        else:
            logging.log(logging.WARNING, "missing multis file, bot will work without reddit fetching commands")

        self.handlers()
        self.updater.start_polling()
        self.updater.idle()
        self.name = name

    def send_content(bot, command, ch_id):
        search = str(command)
        if len(Pybot.arrays[search]) is 0:
            postdata = Pybot.map_r_mr[search].hot()
            for submission in postdata:
                Pybot.arrays[search].append(submission.url)

        cn = Pybot.arrays[search].pop(0)

        try:
            if "v.redd.it/" in cn:
                cn = cn + "/DASH_1_2_M"
                bot.send_video(chat_id=ch_id, video=cn)
                print("vreddit")
            elif "gfycat.com/" in cn:
                splitted = urlsplit(cn)
                path = splitted.path
                if "/detail/" in path:
                    path = path.replace('/detail/', '')
                parsed = "https://thumbs.gfycat.com" + path + "-size_restricted.gif"
                bot.send_video(chat_id=ch_id, video=parsed)
            elif ".gifv" in cn:
                cn = str(cn).replace('.gifv', '.mp4')
                bot.send_video(chat_id=ch_id, video=cn)
            elif ".gif" in cn:
                bot.send_video(chat_id=ch_id, video=cn)

            elif "imgur.com/" or ".jpg" or ".jpeg" or "i.redd.it/" in cn:
                print("jpg or imgur")
                bot.send_photo(chat_id=ch_id, photo=cn)
            else:
                Pybot.send_content(bot, command, ch_id)
        except error.BadRequest:
            logging.log(msg="Error enviando {0} {1} {2}".format(command, ch_id, cn), level=logging.INFO)

        except error.TimedOut:
            bot.send_message(chat_id=ch_id, text="Algo no ha ido bien, prueba /{0} otra vez".format(command))

    # Command method to fetch images and send them to group

    def fetch_reddit(bot, update):
        fetch_command = update.message.text[1:]
        chat_id = update.message.chat_id
        Pybot.send_content(bot, fetch_command, chat_id)

    def list_multis(bot, update):
        key = ''
        for multis in Pybot.map_r_mr.keys():
            key = key + ("/" + multis + "\n")

        bot.send_message(chat_id=update.message.chat_id, text=key)
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
        if str(superid) != None:
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
        meme_gen.mocked(randomized,"memed.jpg")
        bot.send_photo(chat_id=update.message.chat_id, photo=open('memed.jpg', 'rb'))


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


        # Reddit Handlers
        for key, dta in Pybot.map_r_mr.items():
            a = CommandHandler(str(key), Pybot.fetch_reddit)
            Pybot.dispatcher.add_handler(a)
        list_multis_handler = CommandHandler('listmulti', Pybot.list_multis)
        # Mensage Listeners

        echo_handler = MessageHandler(Filters.text, Pybot.echo)
        users_group_handler = MessageHandler(Filters.status_update.new_chat_members, Pybot.new_member)

        # Adding handlers to dispatcher
        Pybot.dispatcher.add_handler(start_handler)
        Pybot.dispatcher.add_handler(about_handler)
        Pybot.dispatcher.add_handler(torrent_handler)
        Pybot.dispatcher.add_handler(facha_handler)
        Pybot.dispatcher.add_handler(users_group_handler)
        Pybot.dispatcher.add_handler(echo_handler)
        Pybot.dispatcher.add_handler(list_multis_handler)


if __name__ == '__main__':
    bot = Pybot('Pyrite')
