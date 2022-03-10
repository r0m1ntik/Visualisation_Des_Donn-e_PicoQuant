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

# Types de balises
tyEmpty8 = struct.unpack(">i", bytes.fromhex("FFFF0008"))[0]
tyBool8 = struct.unpack(">i", bytes.fromhex("00000008"))[0]
tyInt8 = struct.unpack(">i", bytes.fromhex("10000008"))[0]
tyBitSet64 = struct.unpack(">i", bytes.fromhex("11000008"))[0]
tyColor8 = struct.unpack(">i", bytes.fromhex("12000008"))[0]
tyFloat8 = struct.unpack(">i", bytes.fromhex("20000008"))[0]
tyTDateTime = struct.unpack(">i", bytes.fromhex("21000008"))[0]
tyFloat8Array = struct.unpack(">i", bytes.fromhex("2001FFFF"))[0]
tyAnsiString = struct.unpack(">i", bytes.fromhex("4001FFFF"))[0]
tyWideString = struct.unpack(">i", bytes.fromhex("4002FFFF"))[0]
tyBinaryBlob = struct.unpack(">i", bytes.fromhex("FFFFFFFF"))[0]

# Types de record
rtPicoHarpT3 = struct.unpack(">i", bytes.fromhex('00010303'))[0]

# Declanchage du compteur de temps écoulé
t.tic()

# Variables global
global recNum, inputfile, outputfile, oflcorrection, truensync, dlen, isT2, globRes, numRecords, TPP, debutlignetime, indentation, createjson

if __name__ == "__main__":
    argv = sys.argv[0:]
    if len(sys.argv) < 3:
        print("USAGE: python3 main.py -i data/pt3/SRV_2.pt3 -o ./data/json/SRV_2.json")
        exit(0)
    try:
        opts, args = getopt.getopt(argv, "hij")
    except getopt.GetoptError:
        print(f'{sys.argv[0]} -i <inputfile> -o <outputfile>')
        sys.exit(2)

    for opt, arg in opts:
        print("fgchgvjhklml")
        if opt in ("-h", "--help"):
            print('test.py -i <inputfile> -o <outputfile>')
            sys.exit(2)
        elif opt in ("-j", "--json"):
            print('test.py -i <inputfile> -o <outputfile>')
            createjson = arg
        elif opt in ("-i", "--indent"):
            indentation = True

# creation de json enable par defaut
createjson = True
# indentation disable par defaut
indentation = False

# Lecture du 2eme argument (r : lecture - b : format binaire)
inputfile = open(sys.argv[1], "rb")

# Les éléments suivants sont nécessaires pour la prise en charge des chaînes larges
outputfile = io.open(sys.argv[2], "w+", encoding="utf-8")

# Vérifiez si le fichier d'entrée est un fichier PTU valide
# Les chaînes Python n'ont pas de caractères NULL de fin, elles sont donc supprimées
Ident = inputfile.read(16).decode("utf-8").strip('\0')

# Vérification du format du fichier
if Ident != "PicoHarp 300":
    print("ERREUR: Ce n'est pas un fichier PT3.")
    inputfile.close()
    outputfile.close()
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
inputfile.read(32)
# TPP = struct.unpack("<i", inputfile.read(4))[0] / 1e6
# TPP = 1004
TPP = 982.33
inputfile.read(108)

# get important variables from headers
numRecords = Record
globRes = Resol

print("Écriture de {}%d{} enregistrements, cela peut prendre un certain temps...".format(
    color.RED_HL, color.END) % numRecords)


def readPT3():
    global inputfile, outputfile, recNum, oflcorrection, dlen, numRecords, debutlignetime
    global pt, lg, px, Data, img
    debutimg = False
    debutligne = False
    oflcount = 0
    T3WRAPAROUND = 65536
    numpixel = 0
    numligne = 0
    numimg = 0
    i = 0
    Data["file"] = sys.argv[1]

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
                    lg["nlg"] = numligne
                    img["lg"].append(copy.copy(lg))
                    lg["px"] = []
                    if numligne == 32:
                        img["nimg"] = numimg
                        Data["img"].append(copy.copy(img))
                        img["lg"] = []

        else:
            if debutligne:
                if channel == 0 or channel > 4:  # Should not occur
                    print("Illegal Channel: #%1d %1u" % (dlen, channel))
                while(truensync > (debutlignetime + (numpixel)*TPP)):
                    # ecriture du pixel dans la ligne et changement de pixel
                    numpixel += 1
                    lg["px"].append(copy.copy(px))
                    px["px"] = numpixel
                    px["pt"] = []

                # ecriture du photon dans le pixel
                pt["dtime"] = dtime
                pt["nsync"] = truensync
                px["pt"].append(copy.copy(pt))
                pt.clear

                dlen += 1
        if recNum % 100000 == 0:
            sys.stdout.write("\r{}La progression: %.1f%% -- %.5f seconds{}".format(color.GREEN, color.END) %
                             (float(recNum)*100/float(numRecords), t.tocvalue()))
            sys.stdout.flush()


oflcorrection = 0
dlen = 0
print("PicoHarp T3 data")
readPT3()
t.toc('\nLe temps de replissage de la bibliotheque est de', restart=createjson)

# Generation du fichier json
if (createjson):
    print("\nDebut du remplissage fichier...")
    if (indentation):
        json.dump(Data, outputfile, indent=4)
    else:
        json.dump(Data, outputfile)
    t.toc('Temps d\'ecriture en json est de')

# nettoyage du tableau
# Data.clear

inputfile.close()
outputfile.close()
