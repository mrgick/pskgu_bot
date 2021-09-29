import asyncio
from ttf_opensans import OPENSANS_REGULAR, OPENSANS_BOLD
from PIL import Image, ImageDraw
from pskgu_bot.utils import get_week_days, get_name_of_day
import textwrap
from io import BytesIO
from typing import BinaryIO


class COLOR:
    BACKGROUND = "#FFFFFF"
    HEAD_TEXT = "#000000"
    TABLE_TEXT = "#000000"
    LINE = "#000000"


class TEXT_SIZE:
    TABLE = 14
    HEAD = 20


LINE_SIZE = 2


def get_max_word_length(days: dict, keys: list) -> int:
    """
        Находит длину самого длинного слова.
    """
    max_word_len = 0
    for key in keys:
        if days.get(key):
            for _, data in days.get(key).items():
                value = data.split(" ")
                for word in value:
                    if len(word) > max_word_len:
                        max_word_len = len(word)
    return int(max_word_len)


def get_text_xy(size: int) -> int:
    """
        Возвращает значение высоты и ширины
        текста шрифта Open Sans.
    """
    return (size / 2, size * 2)


def draw_horizontal_line(draw: ImageDraw.Draw, max_x: int, y: int) -> None:
    draw.line(xy=(0, y, max_x, y), fill=COLOR.LINE, width=LINE_SIZE)


def draw_row(draw: ImageDraw.Draw, y_now: int, arr: list,
             WEIGHT_COLOMN: int) -> int:
    x_now = 10
    for word in arr:
        draw.text(font=OPENSANS_REGULAR.imagefont(TEXT_SIZE.TABLE),
                  fill=COLOR.TABLE_TEXT,
                  xy=(x_now, y_now),
                  text=word)
        x_now += WEIGHT_COLOMN

    x_now = 0
    y_now += get_text_xy(TEXT_SIZE.TABLE)[1]
    draw_horizontal_line(draw, (WEIGHT_COLOMN * 8 + 1), y_now)
    y_now += LINE_SIZE * 2
    return y_now


async def week_to_image(days: dict,
                        group_name: str,
                        group_prefix: str,
                        week_shift: int = 0) -> BinaryIO:

    days_keys = get_week_days(week_shift)

    MAX_WORD_LENGTH = get_max_word_length(days, days_keys) + 10
    if MAX_WORD_LENGTH < 16:
        MAX_WORD_LENGTH = 16

    WEIGHT_COLOMN = int(MAX_WORD_LENGTH * (TEXT_SIZE.TABLE / 2))
    X_LENGTH = int(WEIGHT_COLOMN * 8 + LINE_SIZE * 7)
    Y_LENGTH = int(3000)

    img = Image.new('RGB', (X_LENGTH, Y_LENGTH), color=COLOR.BACKGROUND)

    draw = ImageDraw.Draw(img)

    # Рисуем заголовок таблицы
    y_now = 0
    x_now = 0
    draw.text(font=OPENSANS_REGULAR.imagefont(TEXT_SIZE.HEAD),
              fill=COLOR.TABLE_TEXT,
              xy=(x_now, y_now),
              text=(group_prefix + ": "))

    x_now = len(group_prefix + ": ") * get_text_xy(TEXT_SIZE.HEAD)[0]
    draw.text(font=OPENSANS_BOLD.imagefont(TEXT_SIZE.HEAD),
              fill=COLOR.HEAD_TEXT,
              xy=(x_now, y_now),
              text=(group_name))

    # Первая верхняя линия
    y_now = get_text_xy(TEXT_SIZE.TABLE)[1]
    x_now = 0
    draw_horizontal_line(draw, (WEIGHT_COLOMN * 8 + 1), y_now)

    # Вертикальные линии
    y_now += LINE_SIZE
    x_now = WEIGHT_COLOMN
    for n in range(0, 8, 1):
        draw.line(xy=(x_now, y_now, x_now, Y_LENGTH),
                  fill=COLOR.LINE,
                  width=LINE_SIZE)
        x_now = x_now + WEIGHT_COLOMN

    # Первая строка
    y_now += LINE_SIZE
    arr = ["Пары", "1-я", "2-я", "3-я", "4-я", "5-я", "6-я", "7-я"]
    y_now = draw_row(draw, y_now, arr, WEIGHT_COLOMN)

    # Вторая строка
    arr = [
        "Время", "08:30-10:00", "10:15-11:45", "12:30-14:00", "14:15-15:45",
        "16:00-17:30", "18:00-19:30", "19:40-21:10"
    ]
    y_now = draw_row(draw, y_now, arr, WEIGHT_COLOMN)

    # Заполнение таблицы данными из days
    for day_date in days_keys:
        x_now = 10
        draw.multiline_text(font=OPENSANS_REGULAR.imagefont(TEXT_SIZE.TABLE),
                            fill=COLOR.TABLE_TEXT,
                            xy=(x_now, y_now),
                            text=(get_name_of_day(day_date) + ",\n" +
                                  day_date))
        if days.get(day_date):
            x_now = WEIGHT_COLOMN + 10
            y_max = 0
            for i in range(1, 8, 1):
                i = str(i)
                if days[day_date].get(i):
                    text = days[day_date][i]
                    lines = textwrap.wrap(text, width=MAX_WORD_LENGTH - 5)
                    y_tmp = 5
                    for line in lines:
                        draw.text(xy=(x_now, y_tmp + y_now),
                                  text=line,
                                  font=OPENSANS_REGULAR.imagefont(
                                      TEXT_SIZE.TABLE),
                                  fill=COLOR.TABLE_TEXT)
                        y_tmp += get_text_xy(TEXT_SIZE.TABLE)[1]
                    if y_tmp > y_max:
                        y_max = y_tmp
                x_now += WEIGHT_COLOMN
            y_now += y_max + 2

        else:
            y_now += get_text_xy(TEXT_SIZE.TABLE)[1] * 2
        if days_keys.index(day_date) != len(days_keys) - 1:
            draw_horizontal_line(draw, (WEIGHT_COLOMN * 8 + 1), y_now)
        y_now += LINE_SIZE

    img = img.crop((0, 0, X_LENGTH, y_now + 50))
    # img = img.resize((int(X_LENGTH / 2), int(y_now / 2)), Image.ANTIALIAS)

    # img.show()

    # await asyncio.sleep(1)
    output = BytesIO()
    img.save(output, format="JPEG")
    return output
