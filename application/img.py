import io
import sys
import getopt
import json
from PIL import Image
from math import *
from tqdm import tqdm
import convert as Dumppt3
import numpy as np
import itertools
import statistics
import matplotlib.pyplot as plt

# creation et initialisation d'un tableau de pixel pour notre image
global Data


def newImg(column, row, TAB_PIXEL):
    k = itertools.chain.from_iterable(TAB_PIXEL)
    v = max(k)
    v = 256/v

    img = Image.new('RGB', size=(column, row))
    for i in range(row):
        for j in range(column):
            color = ceil(TAB_PIXEL[i][j] * v)
            img.putpixel(
                (j, i), (color, color, color))

    return img

##################################################################################################


def getData(min=0, max=None, select=[]):
    global Data
    global TAB_PIXEL
    Resol = Data["Resol"]
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
    TAB_PHOTON = []
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
                nb_photon = len(dataPhoton)
                if (not select):
                    for w in dataPhoton:
                        # incrémentation du nombre de photon
                        TAB_PHOTON.append(w["dtime"]*Resol)
                elif ([j, k] in select):
                    for w in dataPhoton:
                        # incrémentation du nombre de photon
                        TAB_PHOTON.append(w["dtime"]*Resol)
                TAB_PIXEL[j][k] += nb_photon

    print("\nFin de chargement de l'image.")
    return TAB_PIXEL, TAB_PHOTON, column, row

    ##################################################################################################


def affichageImg(min, max):
    test = [[i, j] for i in range(100, 110)for j in range(10, 20)]
    TAB_PIXEL, TAB_PHOTON, column, row = getData(min, max)
    #TAB_PIXEL,TABPHOTON,column, row = getData(min,max,test)

    print("\nDebut de traitement de l'image...")

    wallpaper = newImg(column, row, TAB_PIXEL)
    wallpaper.show()

    k = itertools.chain.from_iterable(TAB_PIXEL)
    a = plt.hist(TAB_PHOTON,
                 bins='auto')
    plt.title("Histogram")
    plt.show()

    print("\nFin de traitement de l'image.\n")


def recupcercle(x=1, y=1, r1=1, r2=2):
    global Data
    res = []
    column, row = Data["X"], Data["Y"]
    for i in range(row):
        for j in range(column):
            d = ceil(sqrt(pow(x-j, 2)+pow(y-i, 2)))

            if (d <= r2 and d > r1):
                res.append([i, j])
    return res


def ecriretxt(chemin="./testec.txt", cheminsource="./test.pt3", x=1, y=1, r1=1, r2=2):
    global Data
    outputfile = io.open(chemin, "w+", encoding="utf-8")
    outputfile.write("#"+cheminsource+"\n")
    outputfile.write("#X,Y=%d,%d\n" % (x, y))
    outputfile.write("#R1=%d\n" % (r1))
    outputfile.write("#R2=%d\n" % (r2))
    outputfile.write("#NBimage=%d\n" % (len(Data["img"])))
    select = recupcercle(x, y, r1, r2)
    for i in range(len(Data["img"])):
        TAB_PIXEL, TABPHOTON, column, row = getData(i, i+1, select)
        outputfile.write(" \n")
        for j in TABPHOTON:
            outputfile.write("%f\n" % (j))
    outputfile.close()


def main(tab):
    for i in tab:
        affichageImg(i[0], i[1])


if __name__ == "__main__":
    name = sys.argv[0]
    argv = sys.argv[1:]
    inputfile = None
    outputfile = None
    Indentation = False
    inputjson = None
    tabimg = None

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

    if ((inputfile == None and inputjson == None) or tabimg == None):
        print(
            'test.py -i <inputfile.pt3>|-j <inputfile.json> -a <[[min,max], ...]>')
        sys.exit(2)

    if inputfile != None:
        Dumppt3.main(inputfile, outputfile, Indentation, name)
        Data = Dumppt3.Data

    if inputjson != None:
        f = open(inputjson)
        Data = json.load(f)

    main(tabimg)
