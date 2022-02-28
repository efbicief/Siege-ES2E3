import PIL
from PIL import Image
import math

def changeColorDepth(image, colorCount):
    # taken from ufp.image
    if image.mode == 'RGB' or image.mode == 'RGBA':
        ratio = 256 / colorCount
        change = lambda value: math.trunc(value/ratio)*ratio
        return PIL.Image.eval(image, change)
    else:
        raise ValueError('Error: Only supports RGB images.')

depth = 4
img_name = input("Enter file name: ")
try:
    img = changeColorDepth(Image.open(img_name), (depth**2))
except:
    print("File", img_name, "not found! Exiting.")
    exit()


print("Adjusting image colour depth...", end = " ")
result = img.convert('P', palette=Image.ADAPTIVE, colors=(2**depth))
print("Done")


print("Determining palette...", end=" ")
width, height = result.size
pixels = []
output_mem = ""
conv = result.convert("RGB")
for y in range(height):
    for x in range(width):
        r,g,b = conv.getpixel((x, y))
        px_colour = (r,g,b)
        if len(pixels) < (2**depth) and px_colour not in pixels:
            pixels.append(px_colour)
        output_mem += str(hex(pixels.index(px_colour)))[2].upper() + " "
    output_mem += "\n"
print("Done")


hcs = ""
print("Palette:")
for colour in pixels:
    col_str = ""
    for val in colour:
        v = str(hex(val))
        if len(v) == 3:
            col_str += "0"
        else:
            col_str += v[2].upper()
    hcs += col_str + " "
print(hcs)


print("Writing .mem files...", end=" ")

pal_file = open("img_palette.mem", 'w')
pal_file.write(hcs)
pal_file.close()

img_file = open("img.mem", 'w')
img_file.write(output_mem)
img_file.close()

print("Done")

result.show()
