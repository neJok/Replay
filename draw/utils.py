from PIL import Image, ImageDraw

def round_image(img, radius):
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), img.size], radius, fill=255)

    rounded_image = Image.new("RGBA", img.size, (0, 0, 0, 0))

    rounded_image.paste(img, (0, 0), mask=mask)
    return rounded_image


def resize_image(image, width):
    w_percent = (width / float(image.size[0]))
    h_size = int((float(image.size[1]) * float(w_percent)))
    resized_image = image.resize((width, h_size), Image.LANCZOS)
    return resized_image


def resize_and_crop(image, target_width, target_height):
    width, height = image.size

    scale = max(target_width / width, target_height / height)

    new_width = int(width * scale)
    new_height = int(height * scale)
    
    resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)
    
    left = (new_width - target_width) / 2
    top = (new_height - target_height) / 2
    right = (new_width + target_width) / 2
    bottom = (new_height + target_height) / 2
    
    cropped_image = resized_image.crop((left, top, right, bottom))
    
    return cropped_image