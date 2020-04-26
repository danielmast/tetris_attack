# Local application imports
from bot.bot import Bot


class Daniel(Bot):
    def __init__(self):
        super().__init__('daniel')


    def get_action(self):
        return 'get drunk'