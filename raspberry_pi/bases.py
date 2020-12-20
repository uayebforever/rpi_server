from abc import ABC, abstractmethod

from PIL.Image import Image


class BaseDisplay(ABC):

    @abstractmethod
    def display(self, image: Image):
        pass

    @abstractmethod
    def backlight_on(self):
        pass

    @abstractmethod
    def backlight_off(self):
        pass