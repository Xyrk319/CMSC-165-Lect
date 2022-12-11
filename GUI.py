from tkinter import *
from customtkinter import *
from PIL import ImageTk, Image
from ImageProcessor import ImageProcessor


class GUI:
    def __init__(self):
        set_appearance_mode("dark")
        set_default_color_theme("green")
        self.window = CTk()
        self.image_processor = None
        self.image_path = None
        self.input_image = False

        # fonts
        self.header_font = CTkFont(size=24, weight="bold")
        self.normal_font = CTkFont(size=16)
        self.count_font = CTkFont(size=18, weight="bold")

        # variables
        self.dark_number = StringVar(self.window)
        self.light_number = StringVar(self.window)

        # frames
        self.image_frame = CTkFrame(self.window, width=650, height=400)
        self.sidebar_frame = CTkFrame(self.window, width=200, corner_radius=0)
        self.light_frame = CTkFrame(self.sidebar_frame, width=160, height=32)
        self.dark_frame = CTkFrame(self.sidebar_frame, width=160, height=32)

        self.header1 = CTkLabel(
            self.sidebar_frame, text="Statistics:", font=self.header_font)
        self.light_header = CTkLabel(
            self.light_frame, text=self.light_number, font=self.count_font)
        self.dark_header = CTkLabel(
            self.dark_frame, text=self.dark_number, font=self.count_font)

        # buttons
        self.file_btn = CTkButton(
            self.window, text="Open File", font=self.normal_font, command=self.fileOpener)
        self.count_light_button = CTkButton(
            self.sidebar_frame, text="Count Light Pollen", font=self.normal_font, command=self.countLight
        )
        self.count_dark_button = CTkButton(
            self.sidebar_frame, text="Count Dark Pollen", font=self.normal_font, command=self.countDark
        )

    def draw(self):
        self.window.title("CMSC 165 - Lecture Project")

        self.image_frame.grid(sticky="w", row=0, column=0,
                              columnspan=4, padx=20, pady=20)
        # self.image_frame.grid_propagate(False)
        self.sidebar_frame.grid(row=0, column=4, rowspan=4, sticky="nesw")
        self.sidebar_frame.grid_propagate(False)

        self.file_btn.grid(sticky="w", row=1, column=0, padx=20, pady=(0, 20))

        self.header1.grid(row=0, column=0, padx=20, pady=(20, 20))
        self.light_frame.grid(row=1, column=0, padx=20)
        self.light_frame.grid_propagate(False)
        self.count_light_button.grid(row=2, column=0, padx=20, pady=(10, 40))
        self.dark_frame.grid(row=3, column=0, padx=20)
        self.dark_frame.grid_propagate(False)
        self.count_dark_button.grid(row=4, column=0, padx=20, pady=(10, 40))

    def loadImageProcessor(self, path):
        self.image_processor = ImageProcessor(path)

    def fileOpener(self):

        # open a file explorer
        # get the file name of the selected file by the user
        filename = filedialog.askopenfilename(
            initialdir="./assets/",
            title="Select a File",
            filetypes=(("JPG Files", "*.jpg"), ("JPEG Files",
                       "*.jpeg"), ("PNG Files", "*.png")),
        )

        # if the file open is succesful
        if filename:
            # We state that there's currently an opened file for the text editor
            self.image_path = filename
            self.loadImageProcessor(filename)
            self.displayImage()
            self.dark_number.set(None)
            self.light_number.set(None)
            self.input_image = True
            txt = ""
            self.updateCount(txt, self.light_header)
            self.updateCount(txt, self.dark_header)

    def countLight(self):
        if self.input_image != False:
            self.image_processor.countLightPollens()
            # connect to backend to get value
            self.light_number.set(self.image_processor.count_light_pollens)
            txt = self.light_number.get()
            self.updateCount(txt, self.light_header)

    def countDark(self):
        if self.input_image != False:
            # connect to backend to get value
            self.image_processor.countDarkPollens()
            self.dark_number.set(self.image_processor.count_dark_pollens)
            txt = self.dark_number.get()
            self.updateCount(txt, self.dark_header)

    def updateCount(self, count, header):
        header.configure(text=count, justify="center")
        header.grid(row=0, column=0, padx=3, pady=3)

    def displayImage(self):
        im = Image.fromarray(self.image_processor.display_img)
        self.img = ImageTk.PhotoImage(image=im)
        label = Label(self.image_frame, image=self.img)
        label.grid(row=0, column=0, padx=3, pady=3, sticky="nesw")
