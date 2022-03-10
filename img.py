from email.policy import default
from PIL import Image
from math import *
from tqdm import tqdm
from main import Data, color
import numpy as np

# couleur RGB - preparation pour la generation
COLOR = [
    [0, 0, 0],        # 0     photon
    [33, 37, 41],     # 1-2   photon
    [52, 58, 64],     # 3-4   photons
    [73, 80, 87],     # 5-6   photons
    [134, 142, 150],  # 7-8   photons
    [173, 181, 189],  # 9-10  photons
    [206, 212, 218],  # 11-12 photons
    [222, 226, 230],  # 13-14 photons
    [233, 236, 239],  # 15+   photons
    [241, 243, 245],  # 20+   photons rouge
    [248, 249, 250]   # 30+   photons vert
]

# creation et initialisation d'un tableau de pixel pour notre image
column, row = 256, 32
global TAB_PIXEL


class img:
    def newImg(column, row):
        global TAB_PIXEL
        img = Image.new('RGB', size=(column, row))
        for i in range(row):
            for j in range(column):
                color = ceil(TAB_PIXEL[i][j] / 2)
                if color >= 8:
                    if color <= 15:
                        if color <= 10:
                            color = 8
                        else:
                            color = 9
                    else:
                        color = 10

                img.putpixel(
                    (j, i), (COLOR[color][0], COLOR[color][1], COLOR[color][2]))
        return img

    ##################################################################################################
    def getData(min=0, max=len(Data["img"])):
        # si valeur max depasse le nombre d'image
        if (max > len(Data["img"]) or min > len(Data["img"])):
            print(
                f"{color.RED_HL}[!] Erreur, il y a au maximum {len(Data['img'])} image(s){color.END}")
            exit(2)
        print("\nDebut de chargement de l'image...\n")
        global TAB_PIXEL
        TAB_PIXEL = [[0 for j in range(column)] for i in range(row)]
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
                    # parcour photon par photon
                    dataPhoton = dataPixel[k]["pt"]
                    for w in range(len(dataPhoton)):
                        # incrémentation du nombre de photon
                        nb_photon += 1
                    TAB_PIXEL[j][k] += nb_photon
                    # affichage des infos
                    # print(f'image: {min} | ligne: {j} | pixel:{k} | nombre de photon: {nb_photon}')

        print("\nFin de chargement de l'image.")
        print("\nDebut de traitement de l'image...")

        wallpaper = img.newImg(column, row)
        wallpaper.show()

        print("\nFin de traitement de l'image.\n")
        ##################################################################################################


# lancement du programme
img.getData(140, 150)
img.getData(190, 200)
img.getData(250, 260)
