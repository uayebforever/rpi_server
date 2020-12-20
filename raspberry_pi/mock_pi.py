from PIL.Image import Image

from raspberry_pi.bases import BaseDisplay


class _TFT240x135(BaseDisplay):
    def display(self, image: Image):
        pass

    def backlight_on(self):
        pass

    def backlight_off(self):
        pass
TFT240x135 = _TFT240x135()
