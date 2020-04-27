# Standard library imports
from abc import ABC, abstractmethod


class Bot(ABC):
    def __init__(self, player):
        self.player = player

    @abstractmethod
    def start(self):
        pass