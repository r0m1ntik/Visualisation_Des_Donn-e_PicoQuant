#!/usr/bin/python3
import config as Config
import os
from lib.toolstip import *
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo, askyesno
import convert as Convert
import json
import img as Img


class CustomFunction():
    def open_file(self, dir):
        global SelectedFile
        filetypes = [("Fichier pt3", ".pt3"), ("Fichier json", ".json")]
        filename = fd.askopenfilename(
            title='Ouvrir un fichier',
            initialdir=dir,
            filetypes=filetypes
        )

        if (filename):
            Config.SelectedFile = filename
            root, extension = os.path.splitext(filename)
            CustomFunction.read_file(self, filename, extension)
            return True
        else:
            showinfo("", "Aucun fichier selectionné !")
            return False

    def generationTxt(self):
        if (Config.SelectedFile == ""):
            showinfo("", "Aucun fichier choisi !")
            return False
        if (not Config.image_cree):
            showinfo("", "Aucune image generée !")
            return False
        if (not Config.couronne_cree):
            showinfo("", "Aucune couronne generée !")
            return False
        else:
            return True

    def save_file(self, dir):
        if (CustomFunction.generationTxt(self)):
            filename = fd.asksaveasfilename(
                title='Sauvegarder le fichier',
                initialdir=dir
            )

            if (filename):
                Config.SaveFile = filename
                root, extension = os.path.splitext(filename)
                Img.ecriretxt(filename, Config.SelectedFile,
                              Config.config_center_x, Config.config_center_y, min(Config.config_rayon_1, Config.config_rayon_2), max(Config.config_rayon_1, Config.config_rayon_2))
                return True
            else:
                showinfo("", "Aucun fichier selectionné !")
                return False

    def read_file(self, filename, extension):
        if (extension == '.pt3'):
            Convert.main(filename)
            showinfo("Chargement...",
                     f"Chargement du fichier est terminer !")
        else:
            f = open(filename)
            Data = json.load(f)

    def select_img(self, min, lenght):
        Img.Data = Convert.Data
        TAB_PIXEL, TAB_PHOTON, colomn, row = Img.getData(min, min+lenght)
        return TAB_PIXEL, colomn, row

    def do_something(self):
        print(f"Menu clicked")

    def do_quit(self):
        res = askyesno(
            'Quitter', "Voulais vous quitter l'application ?\nPenser a sauvegarder le fichier !")
        if res == True:
            Tk.quit(self)

    def do_about(self):
        showinfo("A propos",
                 f"{Config.AppName}\nVersion: {Config.AppVersion}{Config.AppDev}{Config.AppGit}")

    def error_log(self, msg):
        print(f'\033[31m[LOG]: {msg}\033[0m')

    def success_log(self, msg):
        print(f'\033[32m[LOG]: {msg}\033[0m')

    def warning_log(self, msg):
        print(f'\033[33m[LOG]: {msg}\033[0m')
