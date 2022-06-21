#!/usr/bin/python3
from config import *
from lib.function import *
from lib.toolstip import *
from tkinter import PhotoImage


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
                              command=lambda: CustomFunction.do_something(self))
        menu_file.add_separator()
        self.bind_all(
            "<Control-n>", lambda x: CustomFunction.do_something(self))

        ########### NOUVEAU ###########
        menu_file.add_command(label="Ouvrir",
                              underline=0,
                              accelerator="CTRL+O",
                              command=lambda: CustomFunction.open_file(self, dir=OUTPUT_PATH))
        self.bind_all(
            "<Control-o>", lambda x: CustomFunction.open_file(self, dir=OUTPUT_PATH))

        ########### Generer TXT ###########
        menu_file.add_command(label="Generer TXT",
                              underline=0,
                              accelerator="CTRL+S",
                              command=lambda: CustomFunction.save_file(self, dir=OUTPUT_PATH))
        self.bind_all(
            "<Control-s>", lambda x: CustomFunction.save_file(self, dir=OUTPUT_PATH))

        ########### QUITTER ###########
        menu_file.add_separator()
        menu_file.add_command(label="Quitter",
                              underline=0,
                              accelerator="CTRL+Q",
                              command=lambda: CustomFunction.do_quit(self))
        self.bind_all("<Control-q>", lambda x: CustomFunction.do_quit(self))

        menu_bar.add_cascade(label="Fichier", menu=menu_file)

        menu_edit = Menu(menu_bar, tearoff=0)
        menu_edit.add_command(
            label="Annuler", command=lambda: CustomFunction.do_something(self))
        menu_edit.add_separator()
        menu_edit.add_command(
            label="Copier", command=lambda: CustomFunction.do_something(self))
        menu_edit.add_command(
            label="Couper", command=lambda: CustomFunction.do_something(self))
        menu_edit.add_command(
            label="Coller", command=lambda: CustomFunction.do_something(self))
        menu_bar.add_cascade(label="Editer", menu=menu_edit)

        menu_help = Menu(menu_bar, tearoff=0)
        menu_help.add_command(
            label="A propos", command=lambda: CustomFunction.do_about(self))
        menu_bar.add_cascade(label="Aide", menu=menu_help)

        self.config(menu=menu_bar)
