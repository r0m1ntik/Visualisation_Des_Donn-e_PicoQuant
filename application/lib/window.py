#!/usr/bin/python3
from config import *
from lib.toolstip import *
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo, askyesno
from tkinter import Button, PhotoImage


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
                              command=self.do_something)
        menu_file.add_separator()
        self.bind_all("<Control-n>", lambda x: self.do_something())

        ########### NOUVEAU ###########
        menu_file.add_command(label="Ouvrir",
                              underline=0,
                              accelerator="CTRL+O",
                              command=lambda: self.open_file(dir=OUTPUT_PATH))
        self.bind_all("<Control-o>", lambda x: self.open_file(dir=OUTPUT_PATH))

        ########### SAUVEGARDER ###########
        menu_file.add_command(label="Sauvegarder",
                              underline=0,
                              accelerator="CTRL+S",
                              command=self.do_something)
        self.bind_all("<Control-s>", lambda x: self.do_something())

        ########### QUITTER ###########
        menu_file.add_separator()
        menu_file.add_command(label="Quitter",
                              underline=0,
                              accelerator="CTRL+Q",
                              command=lambda: self.do_quit())
        self.bind_all("<Control-q>", lambda x: self.do_quit())

        menu_bar.add_cascade(label="Fichier", menu=menu_file)

        menu_edit = Menu(menu_bar, tearoff=0)
        menu_edit.add_command(label="Annuler", command=self.do_something)
        menu_edit.add_separator()
        menu_edit.add_command(label="Copier", command=self.do_something)
        menu_edit.add_command(label="Couper", command=self.do_something)
        menu_edit.add_command(label="Coller", command=self.do_something)
        menu_bar.add_cascade(label="Editer", menu=menu_edit)

        menu_help = Menu(menu_bar, tearoff=0)
        menu_help.add_command(label="A propos", command=self.do_about)
        menu_bar.add_cascade(label="Aide", menu=menu_help)

        self.config(menu=menu_bar)

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

    def do_something(self):
        print("Menu clicked: save")

    def do_quit(self):
        response = askyesno(
            "Quitter",
            "Voulais vous quitter l'application ?\nPenser a sauvegarder le fichier !"
        )
        QUITTER = True

    def do_about(self):
        showinfo("My title", "My message")

    def do_create_botton(self):
        ######################### BOTTON 1 ########################
        self.button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        self.button_1 = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        self.button_1.place(
            x=75.0,
            y=0.0,
            width=30.0,
            height=30.0
        )
        CreateToolTip(self.button_1, text='Zoom avant')
        ######################## FIN BOTTON 1 ########################

        ######################## BOTTON 2 ########################
        self.button_image_2 = PhotoImage(
            file=relative_to_assets("button_2.png"))
        self.button_2 = Button(
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_2 clicked"),
            relief="flat"
        )
        self.button_2.place(
            x=110.0,
            y=0.0,
            width=30.0,
            height=30.0
        )
        CreateToolTip(self.button_2, text='Zoom arrière')
        ######################## FIN BOTTON 2 ########################

        ######################## BOTTON 3 ########################
        self.button_image_3 = PhotoImage(
            file=relative_to_assets("button_3.png"))
        self.button_3 = Button(
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_3 clicked"),
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
            command=lambda: self.open_file(dir=OUTPUT_PATH),
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

        ######################## BOTTON 5 ########################
        self.button_image_5 = PhotoImage(
            file=relative_to_assets("button_5.png"))
        self.button_5 = Button(
            image=self.button_image_5,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.open_file(dir=OUTPUT_PATH),
            relief="flat"
        )
        self.button_5.place(
            x=343.0,
            y=142.0,
            width=374.0,
            height=197.0
        )
        ######################## FIN BOTTON 5 ########################
