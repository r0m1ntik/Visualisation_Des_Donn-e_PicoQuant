from lib.window import *
from lib.toolstip import *

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Canvas, Entry, Text, Button, PhotoImage

window = MyWindow()

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=720,
    width=1280,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
canvas.create_rectangle(
    1059.0,
    30.0,
    1280.0,
    480.0,
    fill="#EFEFEF",
    outline="")

canvas.create_rectangle(
    0.0,
    30.0,
    1059.0,
    480.0,
    fill="#EFEFEF",
    outline="")

canvas.create_rectangle(
    0.0,
    509.0,
    1280.0,
    720.0,
    fill="#EFEFEF",
    outline="")

canvas.create_rectangle(
    0.0,
    480.0,
    1280.0,
    509.0,
    fill="#C4C4C4",
    outline="")

canvas.create_rectangle(
    0.0,
    0.0,
    1280.0,
    1.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    0.0,
    0.0,
    1280.0,
    30.0,
    fill="#C4C4C4",
    outline="")

image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    1059.0,
    255.99884033203125,
    image=image_image_1
)

# Creation des boutons
window.do_create_botton()
# Autorisation des changer de taille -- disabled
window.resizable(False, False)
window.mainloop()
