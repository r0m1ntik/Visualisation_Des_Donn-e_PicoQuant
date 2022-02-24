# Read_PTU.py    Read PicoQuant Unified Histogram Files
# This is demo code. Use at your own risk. No warranties.
# Keno Goertz, PicoQUant GmbH, February 2018

# Note that marker events have a lower time resolution and may therefore appear 
# in the file slightly out of order with respect to regular (photon) event records.
# This is by design. Markers are designed only for relatively coarse 
# synchronization requirements such as image scanning. 

# T Mode data are written to an output file [filename]
# We do not keep it in memory because of the huge amout of memory
# this would take in case of large files. Of course you can change this, 
# e.g. if your files are not too big. 
# Otherwise it is best process the data on the fly and keep only the results.

import time
import sys
import struct
import io
import json
import copy








# Tag Types
tyEmpty8      = struct.unpack(">i", bytes.fromhex("FFFF0008"))[0]
tyBool8       = struct.unpack(">i", bytes.fromhex("00000008"))[0]
tyInt8        = struct.unpack(">i", bytes.fromhex("10000008"))[0]
tyBitSet64    = struct.unpack(">i", bytes.fromhex("11000008"))[0]
tyColor8      = struct.unpack(">i", bytes.fromhex("12000008"))[0]
tyFloat8      = struct.unpack(">i", bytes.fromhex("20000008"))[0]
tyTDateTime   = struct.unpack(">i", bytes.fromhex("21000008"))[0]
tyFloat8Array = struct.unpack(">i", bytes.fromhex("2001FFFF"))[0]
tyAnsiString  = struct.unpack(">i", bytes.fromhex("4001FFFF"))[0]
tyWideString  = struct.unpack(">i", bytes.fromhex("4002FFFF"))[0]
tyBinaryBlob  = struct.unpack(">i", bytes.fromhex("FFFFFFFF"))[0]

# Record types
rtPicoHarpT3     = struct.unpack(">i", bytes.fromhex('00010303'))[0]


# global variables
global inputfile
global outputfile
global recNum
global oflcorrection
global truensync
global dlen
global isT2
global globRes
global numRecords
global TPP
global debutlignetime
global photon , ligne, pixel, Data, images



photon = { "nsync": 0,
           "truetime": 0,
           "dtime": 0
                    }

pixel ={ 'pixel' : 0,
        'photon' : []
        }

ligne = {
    'numeroligne' : 1,
    'pixel' : []
}

images = {
    "numero_image": 1,
    "ligne": []
}


Data = {
    "fichier": sys.argv[1],
    "image": []
}










if len(sys.argv) != 3:
    print("USAGE: Read_PTU.py inputfile.PT3 outputfile.txt")
    exit(0)

inputfile = open(sys.argv[1], "rb")
# The following is needed for support of wide strings
outputfile = io.open(sys.argv[2], "w+", encoding="utf-8")

# Check if inputfile is a valid PTU file
# Python strings don't have terminating NULL characters, so they're stripped
Ident = inputfile.read(16).decode("utf-8").strip('\0')
if Ident != "PicoHarp 300":
    print("ERROR: Ident invalid, this is not a PT3 file.")
    inputfile.close()
    outputfile.close()
    exit(0)

version = inputfile.read(6).decode("utf-8").strip('\0')
CreatorName = inputfile.read(18).decode("utf-8").strip('\0')
Creatorversion = inputfile.read(12).decode("utf-8").strip('\0')
fileTime = inputfile.read(18).decode("utf-8").strip('\0')
linefeed = inputfile.read(2).decode("utf-8").strip('\0')
Comment = inputfile.read(256).decode("utf-8").strip('\0')


print("version : " + version)
print("CreatorName : " + CreatorName)
print("Creatorversion : " + Creatorversion)

print("fileTime : " + fileTime)
print("linefeed : " + linefeed)
print("Comment : " + Comment)


NoC,BpR,RoutChan,NboBoards,ActCu = struct.unpack("iiiii", inputfile.read(20))

MeasurmentMode,SubMode,RangeNO,Offset,AcquisitionTime  = struct.unpack("iiiii", inputfile.read(20))
StopAt = struct.unpack("<i", inputfile.read(4))[0]
StopOnOvfl = struct.unpack("<i", inputfile.read(4))[0]
restart = struct.unpack("<i", inputfile.read(4))[0]
DisplayLinLog = struct.unpack("<i", inputfile.read(4))[0]
DisplayTimeAxisFrom = struct.unpack("<i", inputfile.read(4))[0]
DisplayTimeAxisTo = struct.unpack("<i", inputfile.read(4))[0]
DisplayCountAxisFrom = struct.unpack("<i", inputfile.read(4))[0]
DisplayCountAxisTo = struct.unpack("<i", inputfile.read(4))[0]


print("NoC : " , NoC)
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


#debutlec block suivant

inputfile.read(184)

Resol = struct.unpack("f", inputfile.read(4))[0]
print("Resol : " , Resol)


inputfile.read(132)


Record = struct.unpack("<i", inputfile.read(4))[0]
print("Record : " , Record)
unuse = struct.unpack("<i", inputfile.read(4))[0]
#inputfile.read(unuse*4)
inputfile.read(32)
TPP = struct.unpack("<i", inputfile.read(4))[0] / 1e6
inputfile.read(108)


# get important variables from headers
numRecords = Record
globRes = Resol

print("Writing %d records, this may take a while..." % numRecords)

def gotOverflow(count):
    global outputfile, recNum
    outputfile.write("%u OFL *   %2x\n" % (recNum, count))

def gotMarker(timeTag, markers):
    global outputfile, recNum
    outputfile.write("%u MAR %2x   %u\n" % (recNum, markers, timeTag))

def gotPhoton(timeTag, channel, dtime,pixel):
    global outputfile, recNum

    outputfile.write("%u CHN %1x     %u     %8.0lf     %10u      %d\n" % (recNum, channel,\
                        timeTag, (timeTag * globRes * 1e9), dtime,pixel))

def readPT3():
    global inputfile, outputfile, recNum, oflcorrection, dlen, numRecords,debutlignetime
    global photon , ligne, pixel, Data, images
    debutimg =False
    debutligne = False
    oflcount = 0
    T3WRAPAROUND = 65536
    numpixel = 0
    numligne = 0
    numimg = 0
    i=0
    for recNum in range(0, numRecords):
        # The data is stored in 32 bits that need to be divided into smaller
        # groups of bits, with each group of bits representing a different
        # variable. In this case, channel, dtime and nsync. This can easily be
        # achieved by converting the 32 bits to a string, dividing the groups
        # with simple array slicing, and then converting back into the integers.
        try:
            recordData = "{0:0{1}b}".format(struct.unpack("<I", inputfile.read(4))[0], 32)
        except:
            print("The file ended earlier than expected, at record %d/%d."\
                  % (recNum, numRecords))
            exit(0)

        channel = int(recordData[0:4], base=2)
        dtime = int(recordData[4:16], base=2)
        nsync = int(recordData[16:32], base=2)
        truensync = (oflcount * T3WRAPAROUND) + nsync

        if channel == 0xF: # Special record
            if dtime == 0: # Not a marker, so overflow
                oflcount += 1
            else:
                #gotMarker(truensync, dtime)
                if dtime == 4:
                    numimg+=1
                    debutligne = 0
                    numligne = 0

                if dtime == 1:
                    debutlignetime = truensync
                    numpixel = 0
                    numligne += 1
                    debutligne = True

                if dtime == 2: 
                    debutligne = False
                    ligne["numeroligne"] = numligne
                    images["ligne"].append(copy.copy(ligne))
                    ligne["pixel"]=[]
                    if numligne == 32 :
                        images["numero_image"]=numimg
                        Data["image"].append(copy.copy(images))
                        images["ligne"]=[]
                        
                    

        else:
            if debutligne:
                if channel == 0 or channel > 4: # Should not occur
                    print("Illegal Channel: #%1d %1u" % (dlen, channel))
                while(truensync > (debutlignetime + (numpixel)*TPP)): 
                    #ecriture du pixel dans la ligne et changement de pixel
                    numpixel += 1
                    ligne["pixel"].append(copy.copy(pixel))
                    pixel["pixel"] = numpixel
                    pixel["photon"]=[]

                #gotPhoton(truensync, channel, dtime,numpixel)
                # ecriture du photon dans le pixel
                photon["dtime"]=dtime
                photon["nsync"]=truensync
                photon["truetime"] = (truensync * globRes * 1e9)
                pixel["photon"].append(copy.copy(photon))
                photon.clear

                dlen += 1
        if recNum % 100000 == 0:

            sys.stdout.write("\rProgress: %.1f%%" % (float(recNum)*100/float(numRecords)))
            sys.stdout.flush()
"""            i+=1
            print(Data)
        if i==3:break
"""

oflcorrection = 0
dlen = 0

print("PicoHarp T3 data")








readPT3()
print("remplissage fichier")
json.dump(Data,outputfile)


inputfile.close()
outputfile.close()



#1001.578125
#1001.57421875