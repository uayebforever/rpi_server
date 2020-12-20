# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw, ImageFont, ImageColor

from utilities import Singleton
from raspberry_pi.bases import BaseDisplay
from raspberry_pi import TFT240x135

from typing import Union, Sequence

BLACK = ImageColor.getrgb("Black")


@Singleton
class Display:
    width = 240
    height = 135

    def __init__(self, hardware_display: BaseDisplay = TFT240x135):
        # Create blank image for drawing.
        # Make sure to create image with mode 'RGB' for full color.
        self._image: Image.Image = Image.new("RGB", (self.width, self.height))
        # Get drawing object to draw on image.
        self._draw: ImageDraw.Draw = ImageDraw.Draw(self._image)

        self._display: BaseDisplay = hardware_display

        self.clear()
        self.backlight_on()

    def backlight_on(self):
        self._display.backlight_on()

    def backlight_off(self):
        self._display.backlight_off()

    def clear(self):
        # Draw a black filled box to clear the image.
        self._draw.rectangle((0, 0, self.width, self.height), outline=0, fill=(0, 0, 0))
        self._display.display(self._image)

    def text(self, messages: Union[str, Sequence]):

        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)

        if isinstance(messages, str):
            messages = (messages,)

        x = 0
        y = -2
        for i, line in enumerate(messages):
            if i > 3:
                break
            self._draw.text((x, y), line, font=font, fill="#FFFFFF")
            y += font.getsize(line)[1]

        self._display.display(self._image)

    def image(self, image: Image):
        my_image = image.convert(mode="RGB")  # returns a defensive copy in correct mode.
        if my_image.size == (self.width, self.height):
            # image is already correct size for display
            self._display.display(my_image)
        else:
            # image must be resized
            self._display.display(self._reduce_image(my_image))

    def _reduce_image(self, my_image):
        if my_image.width > self.width or my_image.height > self.height:
            my_image.thumbnail((self.width, self.height), Image.BILINEAR)
        padded_image = Image.new("RGB", (self.width, self.height), color=BLACK)
        left_pad = (self.width - my_image.width) // 2
        top_pad = (self.height - my_image.height) // 2
        padded_image.paste(my_image, box=(left_pad, top_pad))
        return padded_image
