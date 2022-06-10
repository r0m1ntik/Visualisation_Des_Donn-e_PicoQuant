# This file is part of the VisualisationDesDonnéePicoquant. See AUTHORS file for Copyright information

# This program is free software you can redistribute it and / or modify it
# under the terms of the GNU Affero General Public License as published by the
# Free Software Foundation
# either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY
# without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for
# more details.

# You should have received a copy of the GNU General Public License along
# with this program. If not, see < http: // www.gnu.org/licenses/>.

import sys
import struct
import io
import sys
import getopt
import json
import copy
from math import *

from pytictoc import TicToc


class color:
    BOLD = '\033[1m'
    ITALIC = '\033[3m'
    GRAY = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    CRIMSON = '\033[38m'
    RED_HL = '\033[41m'
    GREEN_HL = '\033[42m'
    BROWN_HL = '\033[43m'
    BLUE_HL = '\033[44m'
    PURPLE_HL = '\033[45m'
    CYAN_HL = '\033[46m'
    GRAY_HL = '\033[47m'
    WHITE_HL = '\033[48m'
    END = '\033[0m'


# Debut du programme
t = TicToc()

# Stucture de stockage
global pt, px, lg, img, Data

# Stockage des photons de chanque pixels
pt = {
    'nsync': 0,
    'dtime': 0
}

# Stockage des pixels de chaque lignes
px = {
    'px': 0,
    'pt': []
}

# Stockage des lignes de chaque images
lg = {
    'nlg': 1,
    'px': []
}

# Stockage des images
img = {
    'nimg': 1,
    'lg': []
}

# Stockage des toutes les données
Data = {
    'file': "",
    'img': []
}

# Declanchage du compteur de temps écoulé
t.tic()

# Variables global
global recNum, inputfile, outputfile, numRecords,  debutlignetime, X, Y


def lectureentete(inputfile):
    global outputfile, recNum, numRecords, debutlignetime, X, Y

    # Vérifiez si le fichier d'entrée est un fichier PTU valide
    # Les chaînes Python n'ont pas de caractères NULL de fin, elles sont donc supprimées
    Ident = inputfile.read(16).decode("utf-8").strip('\0')

    # Vérification du format du fichier
    if Ident != "PicoHarp 300":
        print("ERREUR: Ce n'est pas un fichier PT3.")
        inputfile.close()
        exit(0)

    # Récuperation des données (non utilisé dans le json)
    version = inputfile.read(6).decode("utf-8").strip('\0')
    CreatorName = inputfile.read(18).decode("utf-8").strip('\0')
    Creatorversion = inputfile.read(12).decode("utf-8").strip('\0')
    fileTime = inputfile.read(18).decode("utf-8").strip('\0')
    linefeed = inputfile.read(2).decode("utf-8").strip('\0')
    Comment = inputfile.read(256).decode("utf-8").strip('\0')

    # Affichage des données récuperées
    print("Version: " + version + "\nCreateur: " +
          CreatorName + "\nVersion: " + Creatorversion + "\nDate|Heure: " + fileTime + "\nSaut de ligne: " + linefeed + "\nCommentaire: " + Comment)

    NoC, BpR, RoutChan, NboBoards, ActCu = struct.unpack(
        "iiiii", inputfile.read(20))

    MeasurmentMode, SubMode, RangeNO, Offset, AcquisitionTime = struct.unpack(
        "iiiii", inputfile.read(20))
    StopAt = struct.unpack("<i", inputfile.read(4))[0]
    StopOnOvfl = struct.unpack("<i", inputfile.read(4))[0]
    restart = struct.unpack("<i", inputfile.read(4))[0]
    DisplayLinLog = struct.unpack("<i", inputfile.read(4))[0]
    DisplayTimeAxisFrom = struct.unpack("<i", inputfile.read(4))[0]
    DisplayTimeAxisTo = struct.unpack("<i", inputfile.read(4))[0]
    DisplayCountAxisFrom = struct.unpack("<i", inputfile.read(4))[0]
    DisplayCountAxisTo = struct.unpack("<i", inputfile.read(4))[0]

    print("NoC : ", NoC)
    print("BpR : %d" % BpR)
    print("RoutChan : %d" % RoutChan)
    print("NboBoards : %d" % NboBoards)
    print("ActCu : %d" % ActCu)
    print("MeasurmentMode : %d" % MeasurmentMode)
    print("SubMode : %d" % SubMode)
    print("RangeNO : %d" % RangeNO)
    print("Offset : %d" % Offset)
    print("AcquisitionTime : %d" % AcquisitionTime)
    print("StopAt : %d" % StopAt)
    print("StopOnOvfl : %d" % StopOnOvfl)
    print("restart : %d" % restart)
    print("DisplayLinLog : %d" % DisplayLinLog)
    print("DisplayTimeAxisFrom : %d" % DisplayTimeAxisFrom)
    print("DisplayTimeAxisTo : %d" % DisplayTimeAxisTo)
    print("DisplayCountAxisFrom : %d" % DisplayCountAxisFrom)
    print("DisplayCountAxisTo : %d" % DisplayCountAxisTo)

    # debutlec block suivant

    inputfile.read(184)

    Resol = struct.unpack("f", inputfile.read(4))[0]
    print("Resol : ", Resol)

    inputfile.read(132)

    Record = struct.unpack("<i", inputfile.read(4))[0]
    print("Record : ", Record)
    unuse = struct.unpack("<i", inputfile.read(4))[0]
    # inputfile.read(unuse*4)
    inputfile.read(24)
    X = struct.unpack("<i", inputfile.read(4))[0]
    Y = struct.unpack("<i", inputfile.read(4))[0]
    print(" x: %d  \n y: %d" % (X, Y))
    inputfile.read(108)

    # get important variables from headers
    numRecords = Record

    print("Écriture de {}%d{} enregistrements, cela peut prendre un certain temps...".format(
        color.RED_HL, color.END) % numRecords)


def readPT3(inputfile):
    global outputfile, recNum, numRecords, debutlignetime, name, X, Y
    global pt, lg, px, Data, img
    debutligne = False
    oflcount = 0
    T3WRAPAROUND = 65536
    numpixel = 0
    numligne = 0
    numimg = 0
    i = 0
    TABPHOTON = []
    Data["X"] = X
    Data["Y"] = Y

    for recNum in range(0, numRecords):
        # The data is stored in 32 bits that need to be divided into smaller
        # groups of bits, with each group of bits representing a different
        # variable. In this case, channel, dtime and nsync. This can easily be
        # achieved by converting the 32 bits to a string, dividing the groups
        # with simple array slicing, and then converting back into the integers.
        try:
            recordData = "{0:0{1}b}".format(
                struct.unpack("<I", inputfile.read(4))[0], 32)
        except:
            print("Le dossier s'est terminé plus tôt que prévu, à l'enregistrement %d/%d."
                  % (recNum, numRecords))
            exit(0)

        channel = int(recordData[0:4], base=2)
        dtime = int(recordData[4:16], base=2)
        nsync = int(recordData[16:32], base=2)
        truensync = (oflcount * T3WRAPAROUND) + nsync

        if channel == 0xF:  # Special record
            if dtime == 0:  # Not a marker, so overflow
                oflcount += 1
            else:
                if dtime == 4:
                    numimg += 1
                    debutligne = 0
                    numligne = 0

                if dtime == 1:
                    debutlignetime = truensync
                    numpixel = 0
                    numligne += 1
                    debutligne = True

                if dtime == 2:
                    debutligne = False
                    intervale = (truensync - debutlignetime) / X
                    px["pt"] = []
                    for i in range(X):
                        numpixel += 1
                        px["pt"] = []
                        lg["px"].append(copy.copy(px))
                        px["px"] = numpixel
                    # print(numimg)
                    # print(numligne)
                    for i in TABPHOTON:
                        npx = floor((i["nsync"]-debutlignetime) / intervale)
                        if npx >= X:  # il arrive parfois que la valeur nsync = truesync de fin de ligne
                            npx = X-1
                        pt["dtime"] = i["dtime"]
                        pt["nsync"] = i["nsync"]
                        lg["px"][npx]["pt"].append(copy.copy(pt))

                    TABPHOTON = []
                    lg["nlg"] = numligne
                    img["lg"].append(copy.copy(lg))
                    lg["px"] = []
                    if numligne == Y:
                        img["nimg"] = numimg
                        Data["img"].append(copy.copy(img))
                        img["lg"] = []

        else:
            if debutligne:
                if channel == 0 or channel > 4:  # Should not occur
                    print("Illegal Channel: # %1u" % (channel))
                # stockage du photon
                pt["dtime"] = dtime
                pt["nsync"] = truensync
                TABPHOTON.append(copy.copy(pt))
                pt.clear

        if recNum % 100000 == 0:
            sys.stdout.write("\r{}La progression: %.1f%% -- %.5f seconds{}".format(color.GREEN, color.END) %
                             (float(recNum)*100/float(numRecords), t.tocvalue()))
            sys.stdout.flush()


def main(inputfile, outputfile=None, indentation=False, name="pt3"):
    global recNum, numRecords, debutlignetime

    # Lecture du 2eme argument (r : lecture - b : format binaire)
    inputfile = open(inputfile, "rb")

    print("PicoHarp T3 data")

    Data.clear
    Data["file"] = name
    lectureentete(inputfile)
    readPT3(inputfile)

    inputfile.close()

    t.toc('\nLe temps de replissage de la bibliotheque est de',
          restart=(outputfile != None))

    # Generation du fichier json
    if (outputfile != None):
        outputfile = io.open(outputfile, "w+", encoding="utf-8")
        print("\nDebut du remplissage fichier...")
        if (indentation):
            json.dump(Data, outputfile, indent=4)
        else:
            json.dump(Data, outputfile)
        outputfile.close()
        t.toc('Temps d\'ecriture en json est de')


if __name__ == "__main__":
    name = sys.argv[0]
    argv = sys.argv[1:]
    inputfile = None
    outputfile = None
    Indentation = False

    try:
        opts, args = getopt.getopt(argv, "hi:o:I")
    except getopt.GetoptError:
        print(f'{color.RED_HL}Erreur lors de la recuperation des arguments{color.END}\n'
              f'{sys.argv[0]} -i <inputfile.pt3> -o <outputfile>')
        sys.exit(2)

    for opt, arg in opts:

        if opt in ("-h", "--help"):
            print(f'{color.RED_HL}Pour lancer le programme:\n'
                  f'{sys.argv[0]} -i <inputfile.pt3> -o <outputfile>{color.END}')
            sys.exit(2)
        elif opt in ("-i", "--input"):
            inputfile = arg
        elif opt in ("-o", "--output"):
            outputfile = arg
        elif opt in ("-I", "--indent"):
            Indentation = True

    if (inputfile == None):
        print(f'Champ obligatoire incorrect\n'
              f'{sys.argv[0]} {color.RED_HL}[-i <inputfile.pt3>]{color.END} -o <outputfile> -I')
        sys.exit(2)

    main(inputfile, outputfile, Indentation, name)
