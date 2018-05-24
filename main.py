##
 #  @filename   :   main.cpp
 #  @brief      :   7.5inch e-paper display demo
 #  @author     :   Yehui from Waveshare
 #
 #  Copyright (C) Waveshare     July 28 2017
 #
 # Permission is hereby granted, free of charge, to any person obtaining a copy
 # of this software and associated documnetation files (the "Software"), to deal
 # in the Software without restriction, including without limitation the rights
 # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 # copies of the Software, and to permit persons to  whom the Software is
 # furished to do so, subject to the following conditions:
 #
 # The above copyright notice and this permission notice shall be included in
 # all copies or substantial portions of the Software.
 #
 # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 # FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 # LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 # THE SOFTWARE.
 ##

#import epd7in5
import time
import locale
import weather_api

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageFilter

EPD_WIDTH = 640
EPD_HEIGHT = 384
ROW_COUNT = 3
ROW_WIDTH = EPD_WIDTH / ROW_COUNT
ROW_BORDER_WIDTH = 3


def main():
    # locale.setlocale(locale.LC_ALL, 'de_AT.utf8')
    draw_image()
    """epd = epd7in5.EPD()
    epd.init()

    epd.display_frame(epd.get_frame_buffer(image))"""


def draw_image():
    weather = weather_api.get_current_weather()
    forecasts = weather_api.get_forecast()

    image = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 1)    # 1: clear the frame
    draw = ImageDraw.Draw(image)
    font_big = ImageFont.truetype('Modum.ttf', 60)
    font = ImageFont.truetype('Modum.ttf', 40)
    font_small = ImageFont.truetype('Modum.ttf', 25)

    draw.rectangle((0, 0, EPD_WIDTH, ROW_BORDER_WIDTH), fill=0)
    draw.rectangle((0, EPD_HEIGHT - ROW_BORDER_WIDTH, EPD_WIDTH, EPD_HEIGHT), fill=0)

    icon = Image.open('temperature.bmp', 'r')
    image.resize((32, 32))
    image.paste(icon, (20, 150))

    for x in range(1, ROW_COUNT + 1):

        y_pos = ROW_WIDTH * (x - 1) - ROW_BORDER_WIDTH / 2

        if x == 0:
            y_pos += ROW_BORDER_WIDTH / 2

        draw.rectangle((y_pos, 0, y_pos + ROW_BORDER_WIDTH, EPD_HEIGHT), fill=0)

        y_pos = ROW_WIDTH * x - ROW_BORDER_WIDTH / 2

        if x == ROW_COUNT:
            y_pos -= ROW_BORDER_WIDTH / 2

        draw.rectangle((y_pos, 0, y_pos + ROW_BORDER_WIDTH, EPD_HEIGHT), fill=0)

    draw.text((25, -10), "outdoor", font=font_big, fill=0)
    draw.text((20, 50), "tempature: " + str(weather['temp']) + "°C", font=font_small, fill=0)
    draw.text((20, 80), "humidity: " + str(weather['humidity']) + "%", font=font_small, fill=0)
    draw.text((20, 110), "pressure: " + str(weather['pressure']) + " hPa", font=font_small, fill=0)

    """
    offset = 20
    for cast in forecasts:
        draw.text((220, offset), str(cast['main']['temp']) + u" \u00B0" + "C", font=font, fill=0)

        if len(cast['weather']) > 0:

            offset += 30
            draw.text((220, offset), str(cast['weather'][0]['description']), font=font, fill=0)

        offset += 30
        draw.rectangle((214, offset, 427, offset + 3), fill=0)
        offset += 15
"""
    date = time.strftime("%d.%m.%Y")
    date = date + "\n" + time.strftime("%A")

    draw.multiline_text((460, 20), date, font=font, fill=0, align="center")

    image.save("image.bmp", "BMP")


def draw_forecast(draw):
    pass


if __name__ == '__main__':
    main()
