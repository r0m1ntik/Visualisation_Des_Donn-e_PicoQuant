import itertools
from math import ceil

from numpy import sqrt
from lib.toolstip import *
from lib.function import *
from PIL import ImageTk, Image
from config import relative_to_assets, OUTPUT_PATH, SelectedFile


class MyButton():

    def __init__(self):
        Tk.__init__(self)
        self.do_create_botton(self)

    def do_create_botton(self, canvasG, canvas1, canvas2, canvas3):
        # Varible de zoom (current X1)
        global canva2_x, canva2_y, canva2_img, canva2_cercle, max_x, max_y, img_pos_x, img_pos_y
        global old_x, old_y, oldx, oldy, creation_cercle
        canva2_img = 0
        canva2_cercle = 0
        # pour le cercle
        max_x = 50
        max_y = 50

        # position de l'image
        img_pos_x = 0
        img_pos_y = 0

        canva2_x = int(canvas2['width'])/2
        canva2_y = int(canvas2['height'])/2

        # ACTIVATION DE LA CREATION DU CERCLE
        global centre_x, centre_y, couronne_cree
        global cercle_1_x, cercle_1_y, rayon_1
        global cercle_2_x, cercle_2_y, rayon_2

        creation_cercle = False
        couronne_cree = False

        centre_x = 0
        centre_y = 0
        # CERCLE 1
        cercle_1_x = 0
        cercle_1_y = 0
        rayon_1 = 0
        # CERCLE 2
        cercle_2_x = 0
        cercle_2_y = 0
        rayon_2 = 0

        # d = ceil(sqrt(pow(x-j,2)+pow(y-i,2)))
        # x, y coordonnées du centre
        # j, i coordonnées du points cliqué pour le rayon
        # d le rayon

        ######################## BOTTON 3 ########################
        self.button_image_3 = PhotoImage(
            file=relative_to_assets("button_3.png"))
        self.button_3 = Button(
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("Sauvegarder"),
            relief="flat"
        )
        self.button_3.place(
            x=40.0,
            y=0.0,
            width=30.0,
            height=30.0
        )
        CreateToolTip(self.button_3, text='Sauvegarder')
        ######################## FIN BOTTON 3 ########################

        ######################## BOTTON 4 ########################
        self.button_image_4 = PhotoImage(
            file=relative_to_assets("button_4.png"))
        self.button_4 = Button(
            image=self.button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: general_open(self),
            relief="flat"
        )
        self.button_4.place(
            x=5.0,
            y=0.0,
            width=30.0,
            height=30.0
        )
        CreateToolTip(self.button_4, text='Ouvrir')
        ######################## FIN BOTTON 4 ########################

        ######################## BOTTON 5 ############################
        self.button_image_5 = PhotoImage(
            file=relative_to_assets("button_5.png"))
        self.button_5 = Button(
            image=self.button_image_5,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: general_open(self),
            relief="flat"
        )
        self.button_5.place(
            x=343.0,
            y=142.0,
            width=374.0,
            height=197.0
        )

        ######################## FIN BOTTON 5 ########################

        ######################## BOTTON 6 ############################
        self.button_image_6 = PhotoImage(
            file=relative_to_assets("button_6.png"))
        self.button_6 = Button(
            image=self.button_image_6,
            borderwidth=0,
            highlightthickness=0,
            # command=lambda: creeCercle(
            #     530-max_x, 225-max_y, 530+max_x, 225+max_y),
            command=lambda: activate_create_cercle(self),
            relief="flat"
        )
        self.button_6.place(
            x=250.0,
            y=0.0,
            width=30.0,
            height=30.0
        )
        CreateToolTip(self.button_6, text='Crée un cercle')
        ######################## FIN BOTTON 6 ########################

        ######################## BOTTON 7 ############################
        self.button_image_7 = PhotoImage(
            file=relative_to_assets("button_7.png"))
        self.button_7 = Button(
            image=self.button_image_7,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_7 clicked"),
            relief="flat"
        )
        self.button_7.place(
            x=285.0,
            y=0.0,
            width=30.0,
            height=30.0
        )
        CreateToolTip(self.button_7, text='Agrandir la taille du cercle')
        ######################## FIN BOTTON 7 ########################

        ######################## BOTTON 8 ############################
        self.button_image_8 = PhotoImage(
            file=relative_to_assets("button_8.png"))
        self.button_8 = Button(
            image=self.button_image_8,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_8 clicked"),
            relief="flat"
        )
        self.button_8.place(
            x=320.0,
            y=0.0,
            width=30.0,
            height=30.0
        )
        CreateToolTip(self.button_8, text='Reduire la taille du cercle')
        ######################## FIN BOTTON 8 ########################

        def movement(x, y):
            global img_pos_x, img_pos_y
            canvas2.scan_dragto(x, y, gain=1)
            img_pos_x = x
            img_pos_y = y
            CustomFunction.warning_log(
                self, f'movement avec la souris x={x} y={y}')

        def change_size_cercle(self):
            global max_x, max_y, canva2_cercle

        def activate_create_cercle(self):
            global creation_cercle
            creation_cercle = not creation_cercle
            CustomFunction.success_log(
                self, f"La création du cercle est {('désactivé', 'activé')[creation_cercle]} !")

        def move_cercle(x, y, update=False):
            global canva2_cercle, canva2_img, old_x, old_y, img_pos_x, img_pos_y
            # lorsque on fait un zoom, on garge le cercle au meme endroit
            if (update):
                if (not canva2_cercle):
                    creeCercle(x-max_x, y-max_y, x+max_x, y+max_y)
                    return
                else:
                    # supprimer l'element cercle de canvas2
                    canvas2.delete(canva2_cercle)
                    # on crée le cercle
                    # canvas2.move(canva2_cercle, x-max_x, y-max_y)
                    creeCercle(x-max_x, y-max_y, x+max_x, y+max_y)
            # sinon on le place a la bonne place et on met a jour les coordonées
            else:
                if (canva2_cercle):
                    CustomFunction.warning_log(self, "Cercle est deja crée")
                    return
                else:
                    # supprimer l'element cercle de canvas2
                    canvas2.delete(canva2_cercle)
                    # on crée le cercle
                    # canvas2.move(canva2_cercle, x-max_x, y-max_y)
                    print(
                        f'x:{x} - y:{y} ----- img_pos_x: {img_pos_x} - img_pos_y: {img_pos_y}')
                    if (x != canva2_x):
                        # print("different")
                        # a faire
                        # on annule
                        img_pos_x = 0
                    creeCercle(x-max_x, y-max_y, x+max_x, y+max_y)
                    # affiche le coordonnée
                    print(x, y)
                old_x = x
                old_y = y

        def creeCercle(canva2_x, canva2_y, max_x, max_y):
            global canva2_cercle, old_x, old_y
            canva2_cercle = canvas2.create_oval(
                canva2_x,
                canva2_y,
                max_x,
                max_y,
                width=2,
                # fill="green",
                outline="red"
            )

            old_x = canva2_x
            old_y = canva2_y

            CustomFunction.success_log(
                self, f"Le cercle a été crée à la position x={canva2_x} y={canva2_y}")

        def general_open(self):
            if (CustomFunction.open_file(self, dir=OUTPUT_PATH)):
                TAB_PIXEL, column, row = CustomFunction.select_img(
                    self, 0, 300)
                # print(TAB_PIXEL)
                v = max(itertools.chain.from_iterable(TAB_PIXEL))
                v = 256 / v
                x = 10
                y = 10
                for i in range(Convert.Data["Y"]):
                    for j in range(Convert.Data["X"]):
                        color = ceil(TAB_PIXEL[i][j] * v)
                        color = "#%02x%02x%02x" % (color, color, color)
                        creeCanvaImage(
                            self, x, y, color)
                        x = x + 4
                    x = 10
                    y = y + 4

        def creeCanvaImage(self, x, y, color):
            self.button_5.destroy()
            canvas2.create_rectangle(
                x, y, x+4, y+4, width=0, fill=color)

        canvas2.bind('<ButtonPress-1>',
                     lambda event: onclick(event.x, event.y))

        def onclick(eventx, eventy):
            global centre_x, centre_y, creation_cercle, couronne_cree
            global cercle_1_x, cercle_1_y, rayon_1
            global cercle_2_x, cercle_2_y, rayon_2

            if (not creation_cercle or couronne_cree):
                return

            if (centre_x == 0 or centre_y == 0):
                centre_x = eventx
                centre_y = eventy
                print("Position du centre: x:", eventx, "| y:", eventy)
            else:
                if (cercle_1_x == 0 or cercle_1_y == 0):
                    cercle_1_x = eventx
                    cercle_1_y = eventy
                    rayon_1 = ceil(
                        sqrt(pow(centre_x-eventx, 2)+pow(centre_y-eventy, 2)))
                    creeCercle(centre_x-rayon_1, centre_y -
                               rayon_1, centre_x+rayon_1, centre_y+rayon_1)
                    print("Position du premier cercle: x:",
                          eventx, "| y:", eventy, "| rayon: ", rayon_1)
                else:
                    cercle_2_x = eventx
                    cercle_2_y = eventy
                    rayon_2 = ceil(
                        sqrt(pow(centre_x-eventx, 2)+pow(centre_y-eventy, 2)))
                    creeCercle(centre_x-rayon_2, centre_y -
                               rayon_2, centre_x+rayon_2, centre_y+rayon_2)
                    print("Position du deuxieme cercle: x:",
                          eventx, "| y:", eventy, "| rayon: ", rayon_2)
                    # On met a faut la création du cercle
                    creation_cercle = False
                    couronne_cree = True
                    print("La couronne a bien été crée.")
                    reset_coordonnee()

        def reset_coordonnee(self):
            global cercle_1_x, cercle_1_y, cercle_2_x, cercle_2_y, centre_x, centre_y
            centre_x = 0
            centre_y = 0
            cercle_1_x = 0
            cercle_1_y = 0
            cercle_2_x = 0
            cercle_2_y = 0

            # d = ceil(sqrt(pow(x-j,2)+pow(y-i,2)))
            # x, y coordonnées du centre
            # j, i coordonnées du points cliqué pour le rayon
            # d le rayon
