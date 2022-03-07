from PIL import Image
from tqdm import tqdm
from main import Data

# couleur RGB - preparation pour la generation
COLOR = [
    [0, 0, 0],        # 0     photon
    [23, 32, 42],     # 1-2   photon
    [66, 73, 73],     # 3-4   photons
    [77, 86, 86],     # 5-6   photons
    [98, 101, 103],   # 7-8   photons
    [123, 125, 125],  # 9-10  photons
    [151, 154, 154],  # 11-12 photons
    [208, 211, 212],  # 13-14 photons
    [253, 254, 254]   # 15+   photons
]

TAB_PIXEL = []


class img:
    def newImg(w, h, color):
        img = Image.new('RGB', size=(w, h))
        for i in range(w):
            for j in range(h):
                img.putpixel(
                    (i, j), (COLOR[color][0], COLOR[color][1], COLOR[color][2]))
        return img

    ##################################################################################################
    def getData(min=0, max=len(Data["img"])):
        if (max > 256):
            print(
                "[!] Erreur, le nombre de pixels maximal sur une ligne ne peut pas dépassé 256")
            exit

        print("\nDebut de chargement de l'image...\n")
        # parcour image par image
        dataImg = Data["img"]
        for min in tqdm(range(min, max), desc=f"Chargement des images [{min} à {max}]", ascii=False, ncols=75):
            # parcour ligne par ligne
            dataLigne = dataImg[min]["lg"]
            for j in range(len(dataLigne)):
                # parcour pixel par pixel
                dataPixel = dataLigne[j]["px"]
                for k in range(len(dataPixel)):
                    # init du nombre de photon
                    nb_photon = 0
                    TAB_PIXEL[j, k] = 0
                    # parcour photon par photon
                    dataPhoton = dataPixel[k]["pt"]
                    for w in range(len(dataPhoton)):
                        # incrémentation du nombre de photon
                        nb_photon += 1
                    TAB_PIXEL[j, k] += nb_photon
                    # affichage des infos
                    # print(f'image: {entry} | ligne: {j} | pixel:{k} | nombre de photon: {nb_photon}')
        print("\nFin de chargement de l'image.\n")
        print("\nDebut de traitement de l'image...\n")

        wallpaper = img.newImg(256, 32)
        wallpaper.show()

        for i in range(len(TAB_PIXEL)):
            for y in range(len(TAB_PIXEL[i])):
                print(f'[{i}:{y}]: {TAB_PIXEL[i][y]}')

        print("\nFin de traitement de l'image.\n")
        ##################################################################################################


# lancement du programme
img.getData(5, 10)
