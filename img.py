from PIL import Image
from tqdm import tqdm
from main import Data

# couleur RGB - preparation pour la generation
# 15+   photons - 253, 254, 254
# 11-13 photons - 208, 211, 212
# 9-10  photons - 151, 154, 154
# 7-8   photons - 123, 125, 125
# 5-6   photons - 98, 101, 103
# 3-4   photons - 77, 86, 86
# 1-2   photons - 66, 73, 73
# 0     photon  - 23, 32, 42


class img:
    def newImg(w, h):
        img = Image.new('RGB', size=(w, h))
        for i in range(w):
            for j in range(h):
                img.putpixel((i, j), (i, j, j-i))
        return img

    ##################################################################################################
    def getData(min=0, max=len(Data["img"])):
        print("\nDebut de traitement de l'image...\n")
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
                    # affichage des infos
                    # print(f'image: {entry} | ligne: {j} | pixel:{k} | nombre de photon: {nb_photon}')
        print("\nFin de traitement de l'image.\n")
        ##################################################################################################


# wallpaper = img.newImg(256, 32)
# wallpaper.show()

# lancement du programme
# if __name__ == '__main___':
img.getData(5, 10)
