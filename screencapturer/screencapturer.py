# Standard library imports
from abc import ABC, abstractmethod

# Third party imports
import cv2
import numpy as np
import win32gui, win32ui, win32con, win32api

class ScreenCapturer(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def capture_playfield(self):
        pass