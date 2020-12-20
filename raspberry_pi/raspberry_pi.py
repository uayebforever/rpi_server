__ALL__ = ('TFT240x135',)

import digitalio
import board
from PIL.Image import Image
from adafruit_rgb_display import st7789

# Setup SPI bus using hardware SPI:
from raspberry_pi.bases import BaseDisplay

spi = board.SPI()


class GPIOPins:
    CE0 = digitalio.DigitalInOut(board.CE0)
    D25 = digitalio.DigitalInOut(board.D25)
    D22 = digitalio.DigitalInOut(board.D22)


class _TFT240x135(BaseDisplay):
    # Config for display baudrate (default max is 24mhz):
    _BAUDRATE = 64000000

    # Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
    _cs_pin = GPIOPins.CE0
    _dc_pin = GPIOPins.D25
    _reset_pin = None

    _backlight_pin = GPIOPins.D22

    # Rotation because the actual display is portrait instead of landscape.
    _rotation = 90

    width = 240
    height = 135

    def __init__(self):
        self._backlight_pin.switch_to_output()
        self._backlight_pin.value = True
        self._disp = st7789.ST7789(
            spi,
            cs=self._cs_pin,
            dc=self._dc_pin,
            rst=self._reset_pin,
            baudrate=self._BAUDRATE,
            width=self.height,  # we swap height/width to rotate it to landscape!
            height=self.width,
            x_offset=53,
            y_offset=40,
        )

    def display(self, image: Image):
        if image.size != (self.width, self.height):
            raise ValueError("Image size %s must match display size %s" % (image.size, (self.width, self.height)))
        self._disp.image(image, self._rotation)

    def backlight_on(self):
        self._backlight_pin = True

    def backlight_off(self):
        self._backlight_pin = False
TFT240x135 = _TFT240x135()
