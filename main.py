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

import epd7in5
import Image
import ImageDraw
import ImageFont
import time
import locale
import forecast
#import imagedata

EPD_WIDTH = 640
EPD_HEIGHT = 384


# https://api.openweathermap.org/data/2.5/forecast?q=Innsbruck&units=metric&appid=2678fc5edec0fa22ba8f9d60b5085edc
# https://api.openweathermap.org/data/2.5/weather?q=Innsbruck&units=metric&appid=2678fc5edec0fa22ba8f9d60b5085edc
def main():
    locale.setlocale(locale.LC_ALL, 'de_AT.utf8')
    temp = forecast.get_current_weather()
    forecast.get_forecast()
    epd = epd7in5.EPD()
    epd.init()

    # For simplicity, the arguments are explicit numerical coordinates
    image = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 1)    # 1: clear the frame
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 24)
    draw.rectangle((0, 0, EPD_WIDTH, EPD_HEIGHT), fill=0)
    draw.rectangle((10, 10, EPD_WIDTH - 10, EPD_HEIGHT - 10), fill=255)
    draw.rectangle((214, 10, 216, EPD_HEIGHT - 10), fill=0)
    draw.rectangle((422, 10, 424, EPD_HEIGHT - 10), fill=0)
    draw.text((200, 20), "Test", font=font, fill=0)
    draw.text((20, 20), str(temp) + u" \u00B0" + "C", font=font, fill=0)

    date = time.strftime("%d.%m.%Y")
    date = date + "\n" + time.strftime("%A")

    draw.multiline_text((460, 20), date, font=font, fill=0, align="center")
    epd.display_frame(epd.get_frame_buffer(image))

def draw_forecast(draw):
    pass

if __name__ == '__main__':
    main()
