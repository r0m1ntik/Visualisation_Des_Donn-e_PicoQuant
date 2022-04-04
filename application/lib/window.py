#!/usr/bin/python3
from config import *
from lib.function import *
from lib.toolstip import *
from tkinter import filedialog as fd
from tkinter import Button, PhotoImage

global button_5


class MyWindow(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.create_menu_bar()
        # nom de l'application
        self.title(AppName)
        # forme de l'application
        self.geometry("1280x720")
        # fond de l'application
        self.configure(bg="#FFFFFF")
        # icon
        logo = PhotoImage(file=relative_to_assets("icon.png"))
        self.call('wm', 'iconphoto', self._w, logo)

    def create_menu_bar(self):
        menu_bar = Menu(self)

        ########### NOUVEAU ###########
        menu_file = Menu(menu_bar, tearoff=0)
        menu_file.add_command(label="Nouveau",
                              underline=0,
                              accelerator="CTRL+N",
                              command=CustomFunction.do_something)
        menu_file.add_separator()
        self.bind_all("<Control-n>", lambda x: CustomFunction.do_something())

        ########### NOUVEAU ###########
        menu_file.add_command(label="Ouvrir",
                              underline=0,
                              accelerator="CTRL+O",
                              command=lambda: CustomFunction.open_file(dir=OUTPUT_PATH))
        self.bind_all(
            "<Control-o>", lambda x: CustomFunction.open_file(dir=OUTPUT_PATH))

        ########### SAUVEGARDER ###########
        menu_file.add_command(label="Sauvegarder",
                              underline=0,
                              accelerator="CTRL+S",
                              command=CustomFunction.do_something)
        self.bind_all("<Control-s>", lambda x: CustomFunction.do_something())

        ########### QUITTER ###########
        menu_file.add_separator()
        menu_file.add_command(label="Quitter",
                              underline=0,
                              accelerator="CTRL+Q",
                              command=CustomFunction.do_quit)
        self.bind_all("<Control-q>", lambda x: CustomFunction.do_quit())

        menu_bar.add_cascade(label="Fichier", menu=menu_file)

        menu_edit = Menu(menu_bar, tearoff=0)
        menu_edit.add_command(
            label="Annuler", command=CustomFunction.do_something)
        menu_edit.add_separator()
        menu_edit.add_command(
            label="Copier", command=CustomFunction.do_something)
        menu_edit.add_command(
            label="Couper", command=CustomFunction.do_something)
        menu_edit.add_command(
            label="Coller", command=CustomFunction.do_something)
        menu_bar.add_cascade(label="Editer", menu=menu_edit)

        menu_help = Menu(menu_bar, tearoff=0)
        menu_help.add_command(
            label="A propos", command=CustomFunction.do_about)
        menu_bar.add_cascade(label="Aide", menu=menu_help)

        self.config(menu=menu_bar)
