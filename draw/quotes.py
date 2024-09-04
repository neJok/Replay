import textwrap
from PIL import Image, ImageDraw
from io import BytesIO
from asyncio import gather

from .fonts import montserrat_bold, montserrat_semibold
from .utils import resize_and_crop, round_image

async def draw(data: dict):
    img = Image.open('src/img/frames/quote.png')
    idraw = ImageDraw.Draw(img)

    colors = {
        'black': '#2b2b2b',
    }

    montserrat_bold_144 = montserrat_bold.font_variant(size=144)
    montserrat_semibold_54 = montserrat_semibold.font_variant(size=54)

    async def draw_with_image(news_image):
        with Image.open(news_image) as image:
            image = image.convert("RGBA")
            image = resize_and_crop(image, 1845, 1170)
            rounded_img = round_image(image, 100)
            img.paste(rounded_img, (0, 75), rounded_img)
            
            width, height = image.size
            image = image.crop([0, 0, width // 2, height])
            img.paste(image, (0, 75), image)

        with Image.open('src/img/other/quote_top.png') as quote_top:
            img.paste(quote_top, (0, 0), quote_top)

    async def draw_text(author, text):
        idraw.text((404, 1231), author, colors['black'], montserrat_bold_144)
        
        offset = 42
        x, y = 410, 1370
        for line in textwrap.wrap(text, width=42):
            idraw.text((x, y + offset), line, font=montserrat_semibold_54, fill=colors['black'])
            offset += idraw.textsize(line, font=montserrat_semibold_54)[1]

        
    await gather(
        draw_with_image(data['image']),
        draw_text(data['author'], data['text']),
    )

    return img


async def get_img(data: dict):
    img = await draw(data)

    file = BytesIO()
    img.save(file, "PNG", quality=100)
    file.seek(0)

    return file