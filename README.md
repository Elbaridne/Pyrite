# Pyrite - Telegram bot built in Python
By Mario (Elbaridne) mariomblu.com

### Features:
* Multireddit GIF , Image and Video handling
* Spongebob mock meme if you chat privately with the bot or reply to a message in a group
* MP3 scraping
* /facha (internal joke for my friends)




### Set up:
First of all, you need to create a few files in bot base directory with the following format:
> redditauth
```sh
secret your-secret-api-code
api user pass your-account-password
api user your-account-username
client id your-client-id
user agent your-user-agent-name
```

> config
```sh
your-telegram-api-key
your-own-telegram-id (you can find it with a Telegram bot, not used right now but neccesary)
```

And to get the server up and running, use:
```sh
sudo -s nohup python3
```

You also need the proper url to scrap the mp3 in mp3_scraper (hint: datmusic)

Live at:
    @pyrite_bot

