import epd7in5
import locale
import weather_api
import sensor
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
    epd = epd7in5.EPD()
    epd.init()
    image = draw_image()
    epd.display_frame(epd.get_frame_buffer(image))

def draw_image():
    weather = weather_api.get_current_weather()
    forecasts = weather_api.get_forecast()
    data = sensor.get_data('98:D3:71:F9:66:2B')
    print(data)

    image = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 1)
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

    draw.text((20, 160), "online", font=font_small, fill=0)
    draw.text((20, 180), "tempature: " + str(weather['main']['temp']) + "°C", font=font_small, fill=0)
    draw.text((20, 200), "humidity: " + str(weather['main']['humidity']) + "%", font=font_small, fill=0)
    draw.text((20, 220), "pressure: " + str(weather['main']['pressure']) + " hPa", font=font_small, fill=0)

    draw.text((20, 60), "sensor", font=font_small, fill=0)
    draw.text((20, 80), "tempature: " + str(data['temp']) + "°C", font=font_small, fill=0)
    draw.text((20, 100), "humidity: " + str(data['humidity']) + "%", font=font_small, fill=0)
    draw.text((20, 120), "pressure: " + str(data['pressure'] / 100) + " hPa", font=font_small, fill=0)

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

        offset += 40

    date = time.strftime("%d.%m.%Y")
    date = date + "\n" + time.strftime("%A")

    draw.multiline_text((460, 20), date, font=font, fill=0, align="center")

    draw.text((460, 100), 'sunrise ' + utc_to_local(datetime.utcfromtimestamp(weather['sys']['sunrise'])).strftime('%H:%M'), font=font_small, fill=0)
    draw.text((460, 130), 'sunset ' + utc_to_local(datetime.utcfromtimestamp(weather['sys']['sunset'])).strftime('%H:%M'), font=font_small, fill=0)
    return image


def draw_forecast(draw):
    pass


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

if __name__ == '__main__':
    main()
