# Адаптированная версия Моти для Friendly-Telegram

# Оптимизирован и создан для Heroku

import logging
import os
import io
from base64 import b64decode
from PIL import Image, ImageDraw, ImageFont
from .. import loader, utils

logger = logging.getLogger(__name__)

def register(cb):
    cb(MotyaMod())


@loader.tds
class MotyaMod(loader.Module):
    """Простой и крутой (\U0001F60E) генератор демотиваторов.
Чат и помощь в @motyachat"""

    strings = {
        'name': 'Motya',
        'er_type': ('<code>Тип файла не поддерживается, используйте  '
                    'фото или стикеры</code>'),
        'er_template': ('<code>Произошла ошибка на этапе '
                        'получения темплейта.'
                        ' Подробнее в логе</code>'),
        'er_font': ('<code>Шрифт сказал идти подальше. '
                    'Подробнее в логе</code>'),
        'usage': '<code>.help Motya</code> для помощи',
        'upper_size_cfg_doc': 'Размер шрифта',
        'upper_font_y_cfg_doc': 'Расположение шрифта по вертикали',
        'template_width_cfg_doc': ('Расположение шрифта по горизонтали'
                                   ' (хз почему шрифта лол)'),
        'template_coords_cfg_doc': 'Координаты темплейта',
        'padding_cfg_doc': 'Размеры отступов(padding)'
    }

    def __init__(self):
        self.config = loader.ModuleConfig("upper_size", 45,
                                          lambda: self.strings['upper_size_cfg_doc'],  # noqa: E501
                                          "upper_font_y", 390,
                                          lambda: self.strings['upper_font_y_cfg_doc'],  # noqa: E501
                                          "template_width", 574,
                                          lambda: self.strings['template_width_cfg_doc'],  # noqa: E501
                                          "template_coords", (75, 45, 499,
                                                              373),
                                          lambda: self.strings['template_coords_cfg_doc'],  # noqa: E501
                                          "padding", 10,
                                          lambda: self.strings['padding_cfg_doc'])  # noqa: E501

        self.prename = "premotya.png"
        self.mot_template = 'template.jpg'
        self.upper_font = 'times.ttf'

    async def client_ready(self, client, db):
        self.client = client

    @loader.unrestricted
    async def motyacmd(self, message):
        """Ответьте текстом на картинку или стикер для получения демотиватора"""  # noqa: E501

        # Юзаем байты(извините, у кого нельзя это свернуть...)
        try:
            bytes_template = b'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'  # noqa: e501
            open('template.jpg', 'wb').write(b64decode(bytes_template))
        except Exception as e:
            logger.error(e, exc_info=True)
            await utils.answer(message, self.strings('er_template', message))

        try:
            open('times.ttf', 'wb').write(b64decode(bytes_font))
        except Exception as e:
            logger.error(e, exc_info=True)
            await utils.answer(message, self.strings('er_font', message))

        # Аргументики
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings('usage', message))
            return

        # Сохранение файла
        img = await message.get_reply_message()
        if img and img.media:
            photo = io.BytesIO()
            await self.client.download_media(img, photo)
        else:
            await utils.answer(message, self.strings('usage', message))
            return

        if photo:
            try:
                image = Image.open(photo)
            except OSError:
                await utils.answer(message, self.strings('er_type', message))
                return
            image.save(self.prename, "PNG")
            image.close()

        # Собственно Мотя
        async def draw_x_axis_centered_text(image,
                                            text,
                                            font,
                                            size,
                                            pos_y):
            """Рисование текста демотиватора"""
            draw = ImageDraw.Draw(image)
            text_font = ImageFont.truetype(font, size)
            text_width = text_font.getsize(text)
            while text_width[0] >= self.config['template_width'] - self.config['padding'] * 2:  # noqa: E501
                text_font = ImageFont.truetype(font, size)
                text_width = text_font.getsize(text)
                size -= 1
            draw.text(((self.config['template_width'] - text_width[0]) / 2,
                       pos_y),
                      text,
                      font=text_font)

        async def get_size_from_area(area):
            """Получение размеров"""
            return area[2] - area[0], area[3] - area[1]

        async def make_image():
            """Процессинг изображения"""
            frame = Image.open(self.mot_template)
            demot = Image.open(self.prename)
            demot = demot.resize(await get_size_from_area(self.config['template_coords']),  # noqa: E501
                                 Image.ANTIALIAS)
            frame.paste(demot, self.config['template_coords'])
            await draw_x_axis_centered_text(frame,
                                            args,
                                            self.upper_font,
                                            self.config['upper_size'],
                                            self.config['upper_font_y'])
            img = io.BytesIO()
            img.name = 'motya.png'
            frame.save(img, 'PNG')
            return img

        # Отправка
        demot = await make_image()
        demot.seek(0)
        await utils.answer(message, demot)

        if os.path.isfile(self.prename):
            os.remove(self.prename)
        if os.path.isfile(self.mot_template):
            os.remove(self.mot_template)
        if os.path.isfile(self.upper_font):
            os.remove(self.upper_font)