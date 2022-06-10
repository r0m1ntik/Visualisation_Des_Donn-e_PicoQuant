from lib.window import *
from lib.toolstip import *
from lib.button import MyButton

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Canvas, Entry, Text, Button, PhotoImage

########### Creation de la fenetre global ###########
window = MyWindow()
canvasG = Canvas(
    window,
    height=720,
    width=1280,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvasG.place(x=0, y=0)

########### Grand rectangle GRIS tout en haut ###########
canvasG.create_rectangle(
    0.0,
    0.0,
    1280.0,
    30.0,
    fill="#C4C4C4",
    outline="")
####### BLOCK DE DROITE #######
####### FRAME #######
frame1 = Frame(
    canvasG, bg="#EFEFEF"
)
frame1.place(
    x=1062,
    y=30,
    width=221,
    height=450
)

canvas1 = Canvas(
    frame1,
    bg="#EFEFEF",
    height=450,
    width=221,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas1.place(x=0, y=0)

####### FIN BLOCK DE DROITE #######

####### BLOCK DE GAUCHE #######
frame2 = Frame(
    canvasG,
    bg="#EFEFEF"
)
frame2.place(
    x=0,
    y=30,
    width=1059,
    height=450
)

canvas2 = Canvas(
    frame2,
    bg="#EFEFEF",
    height=450,
    width=1059,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas2.place(x=0, y=0)

####### BLOCK DU BAS #######
frame3 = Frame(
    canvasG, bg="#EFEFEF"
)
frame3.place(
    x=0,
    y=509,
    width=1280,
    height=211
)

canvas3 = Canvas(
    frame3,
    bg="#EFEFEF",
    height=211,
    width=1280,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas3.place(x=0, y=0)

####### BLOCK GRIS DU BAS #######
canvasG.create_rectangle(
    0.0,
    480.0,
    1280.0,
    509.0,
    fill="#C4C4C4",
    outline="")

# Separateur entre bloc droit et gauche
separator = canvasG.create_line(
    1060.0,
    29.0,
    1060.0,
    481,
    width=3,
    fill="#C4C4C4",
    # activefill="#000000" lors du passage de la souris
)

# Creation des boutons
MyButton.do_create_botton(window, canvasG, canvas1, canvas2, canvas3)
# Autorisation des changer de taille -- disabled
window.resizable(False, False)
window.mainloop()
