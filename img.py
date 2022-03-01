from PIL import Image
from main import Data, sys

width = 400
height = 300


def newImg():
    img = Image.new('RGB', size=(256, 32))
    for i in range(1, 256):
        for j in range(0, 32):
            img.putpixel((i, j), (i, i, i))
    return img


print("\nDebut de traitement de l'image...\n")

for j in range(len(Data["img"])+1):
    sys.stdout.write("\rImage trouvé: %0.0f" % jj)
    sys.stdout.flush()

print("\nFin de traitement de l'image\.n")
wallpaper = newImg()
wallpaper.show()
