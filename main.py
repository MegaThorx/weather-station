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
import time
import locale
import weather_api
from datetime import datetime, timedelta, timezone


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
    epd = epd7in5.EPD()
    epd.init()
    image = draw_image()

    epd.display_frame(epd.get_frame_buffer(image))


def draw_image():
    weather = weather_api.get_current_weather()
    forecasts = weather_api.get_forecast()

    image = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 1)    # 1: clear the frame
    draw = ImageDraw.Draw(image)
    font_big = ImageFont.truetype('MonospaceTypewriter.ttf', 40)
    font = ImageFont.truetype('MonospaceTypewriter.ttf', 25)
    font_small = ImageFont.truetype('MonospaceTypewriter.ttf', 15)

    draw.rectangle((0, 0, EPD_WIDTH, ROW_BORDER_WIDTH), fill=0)
    draw.rectangle((0, EPD_HEIGHT - ROW_BORDER_WIDTH, EPD_WIDTH, EPD_HEIGHT), fill=0)


    for x in range(1, ROW_COUNT + 1):

        y_pos = ROW_WIDTH * (x - 1) - ROW_BORDER_WIDTH / 2

        if x == 0:
            y_pos += ROW_BORDER_WIDTH / 2

        draw.rectangle((y_pos, 0, y_pos + ROW_BORDER_WIDTH, EPD_HEIGHT), fill=0)

        y_pos = ROW_WIDTH * x - ROW_BORDER_WIDTH / 2

        if x == ROW_COUNT:
            y_pos -= ROW_BORDER_WIDTH / 2

        draw.rectangle((y_pos, 0, y_pos + ROW_BORDER_WIDTH, EPD_HEIGHT), fill=0)

    draw.text((25, 5), "outdoor", font=font_big, fill=0)
    draw.text((20, 60), "tempature: " + str(weather['main']['temp']) + "°C", font=font_small, fill=0)
    draw.text((20, 80), "humidity: " + str(weather['main']['humidity']) + "%", font=font_small, fill=0)
    draw.text((20, 100), "pressure: " + str(weather['main']['pressure']) + " hPa", font=font_small, fill=0)

    draw.text((225, 5), "forecast", font=font_big, fill=0)

    offset = 60
    for cast in forecasts:
        dt = datetime.strptime(cast['dt_txt'], '%Y-%m-%d %H:%M:%S')
        date_str = dt.strftime('%H:%M')
        dt = dt + timedelta(hours=3)
        date_str = date_str + ' - ' + dt.strftime('%H:%M')
        draw.text((230, offset), date_str, font=font_small, fill=0)
        offset = offset + 20
        draw.text((230, offset), 'temperature: ' + str(cast['main']['temp']) + '°C', font=font_small, fill=0)

        if len(cast['weather']) > 0:
            offset += 20
            draw.text((230, offset), str(cast['weather'][0]['description']), font=font_small, fill=0)

        # icon = Image.open('10d.png', 'r')
        # image.resize((32, 32))
        # image.paste(icon, (20, 150))

        offset += 40

    date = time.strftime("%d.%m.%Y")
    date = date + "\n" + time.strftime("%A")

    draw.multiline_text((460, 20), date, font=font, fill=0, align="center")

    # print(datetime.utcfromtimestamp(weather['sys']['sunrise']))
    # print(utc_to_local(datetime.utcfromtimestamp(weather['sys']['sunrise'])))

    draw.text((460, 100), 'sunrise ' + utc_to_local(datetime.utcfromtimestamp(weather['sys']['sunrise'])).strftime('%H:%M'), font=font_small, fill=0)
    draw.text((460, 130), 'sunset ' + utc_to_local(datetime.utcfromtimestamp(weather['sys']['sunset'])).strftime('%H:%M'), font=font_small, fill=0)

    # image.save("image.bmp", "BMP")
    return image


def draw_forecast(draw):
    pass


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

if __name__ == '__main__':
    main()
