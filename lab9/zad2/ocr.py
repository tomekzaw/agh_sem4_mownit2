from PIL import Image, ImageFont, ImageDraw, ImageOps, ImageChops
import numpy as np
import string
import random
import time
import sys
from collections import defaultdict

def eprint(*args, **kwargs):
    print(*args, file=sys.stdout, **kwargs) # sys.stderr

def trim(img, color='white'):
    background = Image.new(img.mode, img.size, color)
    diff = ImageChops.difference(img, background)
    bbox = diff.getbbox()
    if bbox:
        return img.crop(bbox)
    return img

def ocr(
    image_path='images/Lorem_Arial.png',
    font_family='Arial',
    font_size=40,
    samples=string.ascii_lowercase + string.digits + '?!.,',
    highlight=(-100, 0, -100),
    result_path='results/Lorem_Arial.png',
):
    start = time.time()

    try:
        font = ImageFont.truetype('C:\Windows\Fonts\{}.ttf'.format(font_family), font_size)
    except OSError:
        eprint('Font "{}" not found'.format(font_family))
        raise SystemExit

    image = Image.open(image_path)
    w, h = image.size
    original = np.swapaxes(np.array(ImageOps.invert(image.convert('L'))), 0, 1)
    pixels = image.load()

    original_fft = np.fft.fft2(original)

    recognized = []
    for sample in samples:
        pw, ph = font.getsize(sample)
        imp = Image.new('RGB', (pw, ph), color='white')
        ImageDraw.Draw(imp).text((0, 0), sample, font=font, fill='black')
        #imp = ImageOps.invert(ImageOps.invert(imp).rotate(4, expand=True))
        #imp = trim(imp)
        #imp.save('{}.png'.format(sample))
        pattern = np.swapaxes(np.array(ImageOps.invert(imp.convert('L'))), 0, 1)

        C_pattern = np.max(np.real(
            np.fft.ifft2(
                np.multiply(
                    np.fft.fft2(pattern),
                    np.fft.fft2(np.rot90(pattern, 2))
                )
            )
        ))

        C = np.abs(np.real(
            np.fft.ifft2(
                np.multiply(
                    original_fft,
                    np.fft.fft2(np.rot90(pattern, 2), s=(w, h))
                )
            )
        ) / C_pattern - 1.0)

        C_max_relative_error = 1e-3 if extension == 'png' else 0.02
        """
        if sample in ',.':
            C_max_relative_error *= 0.1
        if sample in 'iIl1':
            C_max_relative_error *= 0.9
        if sample in '!':
            C_max_relative_error *= 0.5
        """

        for x in range(w):
            for y in range(h):
                if C[x][y] < C_max_relative_error:
                    x0, y0 = x-pw, y-ph
                    recognized.append((x0, y0, C[x][y], sample, pw, ph))
                    #pixels[x0,y0] = (255,0,0)

    (i_width, i_height), (space_width, _) = map(font.getsize, ['i', ' '])
    xdiv, ydiv = i_width, i_height // 3
    buckets = defaultdict(dict)
    for one in recognized:
        x, y, C, sample, pw, ph = one
        bx, by = x // xdiv, y // ydiv
        if by not in buckets or bx not in buckets[by] or buckets[by][bx][0] < C:
            buckets[by][bx] = one

    counter = {}
    dr, dg, db = highlight
    for by in sorted(buckets):
        prev = None
        for bx in sorted(buckets[by]):
            x, y, C, sample, pw, ph = buckets[by][bx]

            # insert whitespace
            if prev is not None:
                prev_x, _, _, prev_sample, prev_pw, _ = prev
                if prev_x + prev_pw + space_width * 0.8 < x:
                    print(' ', end='')
            # ignore free commas and dots
            elif sample in ',.':
                continue

            # print recognized character
            print(sample, end='')
            if sample in counter:
                counter[sample] += 1
            else:
                counter[sample] = 1

            # highlight image background
            for dx in range(0, pw+1):
                for dy in range(0, ph+1):
                    x1, y1 = x+dx, y+dy
                    r, g, b = pixels[x1,y1]
                    pixels[x1,y1] = (r+dr, g+dg, b+db)

            prev = buckets[by][bx]

        # insert newline if line is not empty
        if prev is not None:
            print('', end='\r\n')

    """
    # print stats
    end = time.time()
    counter_sum = sum(counter.values())
    counter_count = len(counter)
    eprint('\nFinished in {:.2f} s'.format(end - start))
    eprint('Recognized {} occurrences of {} char{}'.format(counter_sum, counter_count, '' if counter_count == 1 else 's'))
    for i, sample in enumerate(sorted(counter), 0):
        eprint('{}{} ({})'.format('\r\n' if i % 10 == 0 else '\t', sample, counter[sample]), end='')
    eprint('')
    """

    # display image
    image = trim(image)
    if result_path is None:
        image.show()
    else:
        image.save(result_path)

if __name__ == "__main__":
    for font_family in ['Arial', 'Times']:
        #for extension in ['png', 'jpg']:
            extension = 'jpg'
            for example in ['short', 'full']:
                ocr(
                    font_family=font_family,
                    image_path='images/{}_{}.{}'.format(example, font_family, extension),
                    result_path='results/{}_{}.{}'.format(example, font_family, extension),
                    highlight=(-100, 0, -100) if extension == 'png' else (-100, -25, 0)
                )
