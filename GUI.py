from tkinter import *
from customtkinter import *
from PIL import ImageTk, Image
from ImageProcessor import ImageProcessor


class GUI:
    def __init__(self):
        set_appearance_mode("dark")
        set_default_color_theme("green")
        # attributes here
        # self.window = Tk()
        self.window = CTk()
        self.image_processor = None
        self.image_path = None

        # frames
        self.image_frame = CTkFrame(self.window, width=650, height=400)
        self.sidebar_frame = CTkFrame(self.window, width=200, corner_radius=0)

        # buttons
        self.file_btn = CTkButton(self.sidebar_frame, text="Open File", command=self.fileOpener)
        self.count_light_pollen = CTkButton(self.sidebar_frame, text="Count Light Pollen", command=self.countLight)
        self.count_dark_pollen = CTkButton(self.sidebar_frame, text="Count Dark Pollen", command=self.countLight)

        # File opener
        # self.file_opened = False

    def draw(self):
        self.window.title("CMSC 165 - Lecture Project")
        # self.window.geometry("1200x780")

        # component frames
        # self.file_frame = Frame(self.window, width=450, height=50, relief="sunken", background="black")
        # self.img = None
        # self.button_frame = Frame(self.window)

        # buttons

        self.image_frame.grid(row=0, column=1, columnspan=4, padx=20, pady=20)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nesw")
        self.file_btn.grid(sticky="w", row=0, column=0, padx=20, pady=10)
        self.count_light_pollen.grid(sticky="w", row=1, column=0, padx=20, pady=10)
        self.count_dark_pollen.grid(sticky="w", row=2, column=0, padx=20, pady=10)

        # self.file_frame.place(x=10, y=15)
        # self.button_frame.place(x=10, y=50)
        # frame
        # count pollens

    def loadImageProcessor(self, path):
        self.image_processor = ImageProcessor(path)

    def fileOpener(self):

        # open a file explorer
        # get the file name of the selected file by the user
        filename = filedialog.askopenfilename(
            initialdir="./assets/",
            title="Select a File",
            filetypes=(("JPG Files", "*.jpg"), ("JPEG Files", "*.jpeg"), ("PNG Files", "*.png")),
        )

        # if the file open is succesful
        if filename:
            # We state that there's currently an opened file for the text editor
            self.image_path = filename
            self.loadImageProcessor(filename)
            self.displayImage()
        # pass

    def countLight(self):
        pass

    def countDark(self):
        pass

    def displayImage(self):
        im = Image.fromarray(self.image_processor.display_img)
        self.img = ImageTk.PhotoImage(image=im)
        label = Label(self.image_frame, image=self.img)
        label.grid(row=0, column=0, padx=10, pady=10, sticky="nesw")
