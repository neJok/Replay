import textwrap
from PIL import Image, ImageDraw
from io import BytesIO
from asyncio import gather

from .fonts import montserrat_bolditalic
from .utils import resize_and_crop, round_image

async def draw(data: dict):
    img = Image.new('RGBA', (1920, 1920))
    idraw = ImageDraw.Draw(img)

    colors = {
        'black': '#000000',
    }


    async def draw_with_image(news_image):
        with Image.open(news_image) as image:
            image = image.convert("RGBA")
            image = resize_and_crop(image, 1870, 1870)
            img.paste(image, (25, 25), image)
            
        with Image.open('src/img/other/news_top.png') as news_top:
            img.paste(news_top, (0, 0), news_top)

    def wrap_text(text, font, max_width):
        # Разбиваем текст на слова
        words = text.split()
        
        # Переменные для хранения текущей строки и всех строк
        lines = []
        current_line = ""
        
        for word in words:
            # Создаем временную строку для измерения ширины
            test_line = current_line + word + " " if current_line else word
            # Измеряем ширину строки с учетом текущего шрифта
            width, _ = font.getsize(test_line)
            
            # Если ширина строки превышает максимальную ширину, переносим строку
            if width > max_width:
                lines.append(current_line.strip())
                current_line = word + " "
            else:
                current_line = test_line
        
        # Добавляем последнюю строку
        if current_line:
            lines.append(current_line.strip())
        
        return lines

    async def draw_text(text):
        offset = 120

        x, y = 950, 1300
        for i in range(20, 200)[::-1]:
            print(i)
            lines = textwrap.wrap(text, width=round(1920 / (i - 20)))
            if len(lines) * i >= 400:
                continue
            
            font = montserrat_bolditalic.font_variant(size=i)
            for line in lines:
                idraw.text((x, y + offset), line, font=font, fill=colors['black'], anchor="mm")
                offset += idraw.textsize(line, font=font)[1]

            break

        
    await gather(
        draw_with_image(data['image']),
        draw_text(data['text']),
    )

    return img


async def get_img(data: dict):
    img = await draw(data)

    file = BytesIO()
    img.save(file, "PNG", quality=100)
    file.seek(0)

    return file