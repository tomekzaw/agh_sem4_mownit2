from PIL import Image, ImageFont, ImageDraw, ImageOps, ImageChops
import string

def generate_image(
    text='Lorem ipsum sit dolor amet.',
    font_family='Arial',
    font_size=40,
    path='images/Lorem_Arial.png'
):
    font = ImageFont.truetype('C:\Windows\Fonts\{}.ttf'.format(font_family), font_size)
    width, height = 0, 0
    for line in text.split('\n'):
        w, h = font.getsize(line)
        width = max(width, w)
        height += h
    image = Image.new('RGB', (width, height), color='white')
    ImageDraw.Draw(image).text((0, 0), text, font=font, fill='black')
    #image = ImageOps.invert(ImageOps.invert(image).rotate(4, expand=True))
    image = ImageOps.expand(image, border=30, fill='white')
    image.save(path)

if __name__ == "__main__":
    for font_family in ['Arial', 'Times']:
        for extension in ['png', 'jpg']:
            generate_image(
                text='lorem ipsum sit dolor amet.',
                font_family=font_family,
                path='images/short_{}.{}'.format(font_family, extension)
            )

            generate_image(
                text='\n'.join([
                    ' '.join([string.ascii_lowercase, string.digits, '?!.,']),
                    'lorem ipsum dolor sit amet, consectetur adipiscing elit.',
                    'etiam arcu felis, dictum id molestie nec, sagittis quis massa.'
                ]),
                font_family=font_family,
                path='images/full_{}.{}'.format(font_family, extension)
            )