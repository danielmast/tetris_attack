from bot import Bot


class Laurens(Bot):
    def __init__(self):
        super().__init__('laurens')


    def get_action(self):
        return 'study'
