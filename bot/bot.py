# Standard library imports
from abc import ABC, abstractmethod


class Bot(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def get_action(self):
        pass