from abc import ABC, abstractmethod


class Input(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def do_action(self, player, action):
        pass
