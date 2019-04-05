import threading
import signal
import time

from QAuthor import QAuthor
from QGame import QGame


class BotThread(threading.Thread):
    def __init__(self, bot):
        threading.Thread.__init__(self)
        self.shutdown_flag = threading.Event()
        self.bot = bot

    def run(self):
        print(self.bot.__name__ + ' started')

        while not self.shutdown_flag.is_set():
            self.bot.start_polling(True)
        self.bot.stop_polling()
        print(self.bot.__name__ + ' stopped')


class ServiceExit(Exception):
    pass


def service_shutdown(signum, frame):
    print('Caught signal %d' % signum)
    raise ServiceExit


def main():
    signal.signal(signal.SIGTERM, service_shutdown)
    signal.signal(signal.SIGINT, service_shutdown)
    try:
        auth = QAuthor("./configs/qauthor_config.yaml")
        auth_tread = BotThread(auth)  # threading.Thread(target=auth.start_polling, args=[True])

        game = QGame("./configs/qgame_config.yaml")
        game_tread = BotThread(game)  # threading.Thread(target=game.start_polling, args=[True])

        auth_tread.start()
        game_tread.start()

        while True:
            time.sleep(0.5)

    except ServiceExit:
        auth_tread.shutdown_flag.set()
        game_tread.shutdown_flag.set()

        auth_tread.join()
        game_tread.join()


if __name__ == "__main__":
    main()
    #game = QGame("./configs/qgame_config.yaml")
    #game.start_polling(False)

    #auth = QAuthor("./configs/qauthor_config.yaml")
    #auth.start_polling((False))