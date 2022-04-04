#!/usr/bin/python3
from config import *
from lib.toolstip import *
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo, askyesno


class CustomFunction():
    def open_file(self, dir):
        filetypes = [("Fichier pt3", ".pt3"), ("Fichier json", ".json")]
        filename = fd.askopenfilename(
            title='Ouvrir un fichier',
            initialdir=dir,
            filetypes=filetypes
        )
        showinfo(
            title='Fichier pt3 / json',
            message=filename
        )

        SelectedFile = filename

    def do_something(self):
        print(f"Menu clicked")

    def do_quit(self):
        res = askyesno(
            'Quitter', "Voulais vous quitter l'application ?\nPenser a sauvegarder le fichier !")
        if res == True:
            Tk.quit(self)

    def do_about(self):
        showinfo("A propos",
                 f"{AppName}\nVersion: {AppVersion}{AppDev}{AppGit}")
