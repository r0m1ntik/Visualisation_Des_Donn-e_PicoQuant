from lib.toolstip import *
from lib.function import CustomFunction
from PIL import ImageTk, Image
from config import relative_to_assets, OUTPUT_PATH, SelectedFile


class MyButton():

    def __init__(self):
        Tk.__init__(self)
        self.do_create_botton(self)

    def do_create_botton(self, canvasG, canvas1, canvas2, canvas3):
        # Varible de zoom (current X1)
        global current_zoom, current_img, canva2_x, canva2_y, canva2_img, canva2_cercle, max_x, max_y, img_pos_x, img_pos_y
        global old_x, old_y, oldx, oldy
        current_zoom = 1
        current_img = "test.png"
        canva2_img = 0
        canva2_cercle = 0
        # pour le cercle
        max_x = 50
        max_y = 50

        # position de l'image
        img_pos_x = 0
        img_pos_y = 0

        canva2_x = int(canvas2['width'])/2,
        canva2_y = int(canvas2['height'])/2,

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
            # command=lambda: CustomFunction.open_file(self, dir=OUTPUT_PATH),
            command=lambda: creeCercle(
                canva2_x[0]-max_x, canva2_y[0]-max_x, max_x, max_y),
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
            canva2_img = canvas2.create_image(
                canva2_x[0],
                canva2_y[0],
                image=self.loading,
            )

            canvas2.bind("<MouseWheel>", do_zoom)
            canvas2.bind('<ButtonPress-2>',
                         lambda event: move_cercle(event.x, event.y))
            canvas2.bind('<ButtonPress-1>',
                         lambda event: canvas2.scan_mark(event.x, event.y))
            canvas2.bind("<B1-Motion>",
                         lambda event: movement(event.x, event.y))

        def movement(x, y):
            global img_pos_x, img_pos_y
            canvas2.scan_dragto(x, y, gain=1)
            img_pos_x = x
            img_pos_y = y
            print(f'movement: {x} {y}')

        def move_cercle(x, y, update=False):
            global canva2_cercle, canva2_img, old_x, old_y
            if (update):
                if (not canva2_cercle):
                    print("Cercle created")
                    creeCercle(x-max_x, y-max_y, x+max_x, y+max_y)
                    return
                else:
                    # supprimer l'element cercle de canvas2
                    canvas2.delete(canva2_cercle)
                    # on crée le cercle
                    # canvas2.move(canva2_cercle, x-max_x, y-max_y)
                    creeCercle(x-max_x, y-max_y, x+max_x, y+max_y)
            else:
                # supprimer l'element cercle de canvas2
                canvas2.delete(canva2_cercle)
                # on crée le cercle
                # canvas2.move(canva2_cercle, x-max_x, y-max_y)
                creeCercle(x-max_x, y-max_y, x+max_x, y+max_y)
                # affiche le coordonnée
                print(x, y)
                old_x = x
                old_y = y

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
            global current_img, current_zoom, canvas2_img, max_x, max_y, canva2_cercle
            global old_x, old_y
            current_zoom = current
            old = Image.open(relative_to_assets(current_img))
            width, height = old.size
            width = int(width * current_zoom)
            height = int(height * current_zoom)
            resized = old.resize(
                (width, height), Image.ANTIALIAS)
            self.loading = ImageTk.PhotoImage(resized)

            # supprimer l'element canva2_img de canvas2
            canvas2.delete(canva2_img)
            # supprimer l'element cercle de canvas2
            # canvas2.delete(canva2_cercle)

            canvas2.create_image(
                canva2_x[0],
                canva2_y[0],
                image=self.loading,
            )

            move_cercle(old_x, old_y, update=True)

        def creeCercle(canva2_x, canva2_y, max_x, max_y):
            global canva2_cercle
            canva2_cercle = canvas2.create_oval(
                canva2_x,
                canva2_y,
                max_x,
                max_y,
                width=2,
                # fill="green",
                outline="red"
            )
