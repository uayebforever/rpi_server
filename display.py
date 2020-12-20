# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw, ImageFont, ImageColor

import digitalio
import board
from adafruit_rgb_display import st7789

from utilities import Singleton

from typing import Union, Tuple, List, Sequence

# Setup SPI bus using hardware SPI:
spi = board.SPI()

BLACK = ImageColor.getrgb("Black")

@Singleton
class Display:

    width = 240
    height = 135

    # Config for display baudrate (default max is 24mhz):
    _BAUDRATE = 64000000
    # Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
    _cs_pin = digitalio.DigitalInOut(board.CE0)
    _dc_pin = digitalio.DigitalInOut(board.D25)
    _reset_pin = None
    _backlight_pin = digitalio.DigitalInOut(board.D22)


    # Rotation because the actual display is portrait instead of landscape.
    _rotation = 90

    # Draw some shapes.
    # First define some constants to allow easy resizing of shapes.
    padding = -2
    top = padding
    bottom = height - padding
    # Move left to right keeping track of the current x position for drawing shapes.
    x = 0

    def __init__(self):
        self._backlight_pin.switch_to_output()

        # Create blank image for drawing.
        # Make sure to create image with mode 'RGB' for full color.
        self._image = Image.new("RGB", (self.width, self.height))
        # Get drawing object to draw on image.
        self._draw = ImageDraw.Draw(self._image)

        # Create the ST7789 display:
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

        self.clear()
        self.backlight_on()

    def backlight_on(self):
        self._backlight_pin.value = True

    def backlight_off(self):
        self._backlight_pin.value = False

    def clear(self):
        # Draw a black filled box to clear the image.
        self._draw.rectangle((0, 0, self.width, self.height), outline=0, fill=(0, 0, 0))
        self._disp.image(self._image, self._rotation)

    def text(self, messages: Union[str, Sequence]):

        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)

        if isinstance(messages, str):
            messages = (messages, )

        x = 0
        y = -2
        for i, line in enumerate(messages):
            if i > 3:
                break
            self._draw.text((x, y), line, font=font, fill="#FFFFFF")
            y += font.getsize(line)[1]

        self._disp.image(self._image, self._rotation)

    def image(self, image: Image):
        my_image = image.convert(mode="RGB")  # returns a defensive copy in correct mode.
        if my_image.size == (self.width, self.height):
            # image is already correct size for display
            self._disp.image(my_image, self._rotation)
        else:
            # image must be resized
            self._disp.image(self._reduce_image(my_image), self._rotation)

    def _reduce_image(self, my_image):
        if my_image.width > self.width or my_image.height > self.height:
            my_image.thumbnail((self.width, self.height), Image.BILINEAR)
        padded_image = Image.new("RGB", (self.width, self.height), color=BLACK)
        left_pad = (self.width - my_image.width) // 2
        top_pad = (self.height - my_image.height) // 2
        padded_image.paste(my_image, box=(left_pad, top_pad))
        return padded_image

