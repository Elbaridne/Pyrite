from bot import Pybot

if __name__ == '__main__':
    u_case = Pybot('Testing')
    dispatch = u_case.dispatcher
    bot = dispatch.bot
    print(bot.getMe)

    while(True):
        print("1. Comandos 2.Handlers 3.String")
        input("Funcionalidad a probar")

