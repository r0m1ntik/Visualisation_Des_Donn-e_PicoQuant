from email.policy import default
import sys
import getopt
import json
from PIL import Image
from math import *
from tqdm import tqdm
import main as Dumppt3
import numpy as np
import itertools
import statistics

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

]

# creation et initialisation d'un tableau de pixel pour notre image
global TAB_PIXEL, Data


class img:
    global Data

    def newImg(column, row):
        global TAB_PIXEL
        k = itertools.chain.from_iterable(TAB_PIXEL)
        v = statistics.median(k) / 2

        img = Image.new('RGB', size=(column, row))
        for i in range(row):
            for j in range(column):
                color = ceil(TAB_PIXEL[i][j] / v)
                if color >= 8:
                    color = 8
                img.putpixel(
                    (j, i), (COLOR[color][0], COLOR[color][1], COLOR[color][2]))
        return img

    ##################################################################################################
    def getData(min=0, max=None):
        if max == None:
            max = min+5

        column, row = Data["X"], Data["Y"]

        # si valeur max depasse le nombre d'image
        if (max > len(Data["img"]) or min > len(Data["img"])):
            print(
                f"{Dumppt3.color.RED_HL}[!] Erreur, il y a au maximum {len(Data['img'])} image(s){Dumppt3.color.END}")
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


def main(tab):
    for i in tab:
        img.getData(i[0], i[1])


if __name__ == "__main__":
    name = sys.argv[0]
    argv = sys.argv[1:]
    inputfile = None
    outputfile = None
    Indentation = False
    inputjson = None

    try:
        opts, args = getopt.getopt(argv, "hi:o:j:Ia:")
    except getopt.GetoptError:
        print(
            f'{sys.argv[0]} -i <inputfile.pt3>|-j <inputfile.json> -o <outputfile> -a <[[min,max],...]>')
        sys.exit(2)
    for opt, arg in opts:

        if opt in ("-h", "--help"):
            print('{}Pour lancer le programme:{}\n'
                  f'{sys.argv[0]} -i <inputfile.pt3> -j <inputfile.json> -o <outputfile> -a <[[min,max],...]>'.format(Dumppt3.color.RED_HL, Dumppt3.color.END))
            sys.exit(2)
        elif opt in ("-i", "--input"):
            inputfile = arg
        elif opt in ("-o", "--output"):
            outputfile = arg
        elif opt in ("-I", "--indent"):
            Indentation = True
        elif opt in ("-j", "--json"):
            inputjson = arg
        elif opt in ("-a", "-affichage"):
            tabimg = eval(arg)

    if (inputfile == None and inputjson == None):
        print('test.py -i <inputfile.pt3>|-j <inputfile.json>')
        sys.exit(2)

    if inputfile != None:
        Dumppt3.main(inputfile, outputfile, Indentation, name)
        Data = Dumppt3.Data

    if inputjson != None:
        f = open(inputjson)
        Data = json.load(f)

    main(tabimg)
