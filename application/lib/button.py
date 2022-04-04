from lib.toolstip import *
from lib.function import CustomFunction
from PIL import ImageTk, Image
from config import relative_to_assets, OUTPUT_PATH, SelectedFile


class MyButton():

    # Varible de zoom (current X1)
    global current_zoom, current_img
    current_zoom = 1
    current_img = "test.png"

    def __init__(self):
        Tk.__init__(self)
        self.do_create_botton(self)

    def do_create_botton(self, canvasG, canvas1, canvas2, canvas3):
        ######################### BOTTON 1 ########################
        self.button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        self.button_1 = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: zoom(current_zoom + 0.1),
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
            command=lambda: zoom(current_zoom - 0.1),
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
            command=lambda: Change_Pic(self, current_img),
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
            command=lambda: CustomFunction.open_file(self, dir=OUTPUT_PATH),
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
            command=lambda: CustomFunction.open_file(self, dir=OUTPUT_PATH),
            relief="flat"
        )
        self.button_5.place(
            x=343.0,
            y=142.0,
            width=374.0,
            height=197.0
        )
        ######################## FIN BOTTON 5 ########################

        def Change_Pic(self, img):
            self.button_5.destroy()
            old = Image.open(relative_to_assets(img))
            width, height = old.size
            width = width ** current_zoom
            height = height ** current_zoom
            resized = old.resize(
                (width, height), Image.ANTIALIAS)
            self.loading = ImageTk.PhotoImage(resized)
            # self.loading = ImageTk.PhotoImage(
            #     file=relative_to_assets(img))

            # Disposition de l'image dans le canvas2
            canvas2.create_image(
                int(canvas2['width'])/2,
                int(canvas2['height'])/2,
                image=self.loading,
            )

            canvas2.bind("<MouseWheel>", do_zoom)
            canvas2.bind('<ButtonPress-1>',
                         lambda event: canvas2.scan_mark(event.x, event.y))
            canvas2.bind("<B1-Motion>",
                         lambda event: canvas2.scan_dragto(event.x, event.y, gain=1))

        def do_zoom(event):
            global current_zoom
            zoom_in = True
            if (event.delta < 0):
                zoom_in = False
            if (not zoom_in and current_zoom < 5 and current_zoom >= 0.1):
                zoom(current_zoom + 0.1)
            if (zoom_in and current_zoom <= 5 and current_zoom > 0.1):
                zoom(current_zoom - 0.1)
            if (current_zoom < 0.1):
                current_zoom = 0.1
            if (current_zoom > 5):
                current_zoom = 5

        def zoom(current):
            global current_img, current_zoom
            current_zoom = current
            old = Image.open(relative_to_assets(current_img))
            width, height = old.size
            width = int(width * current_zoom)
            height = int(height * current_zoom)
            resized = old.resize(
                (width, height), Image.ANTIALIAS)
            self.loading = ImageTk.PhotoImage(resized)
            canvas2.create_image(
                int(canvas2['width'])/2,
                int(canvas2['height'])/2,
                image=self.loading,
            )
