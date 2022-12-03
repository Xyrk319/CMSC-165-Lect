from tkinter import filedialog
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from ImageProcessor import ImageProcessor


class GUI:

    def __init__(self):

        # attributes here
        self.window = Tk()
        self.window.title("CMSC 165 - Lecture Project")
        self.window.geometry("1200x780")
        self.image_processor = None

        self.image_path = None

        # File opener
        self.file_opened = False

        # File Explorer
        self.file_frame = Frame(self.window, width=450,
                                height=50, relief="sunken", background="black")
        self.file_frame.place(x=10, y=15)
        self.file_btn = Button(self.file_frame, text="Open File",
                               command=self.fileOpener, pady=5).pack()

        # count pollens
        # frame
        self.button_frame = Frame(self.window)

        self.button_frame.place(x=10, y=50)

        # buttons
        self.count_light_pollen = Button(
            self.button_frame, text="Count Light Pollen", command=self.countLight, padx=5, pady=5).pack(pady=10)
        self.count_dark_pollen = Button(
            self.button_frame, text="Count Dark Pollen", command=self.countDark, padx=5, pady=5).pack(pady=10)

        # textbox

        # images

        self.image_frame = Frame(self.window, width=650,
                                 height=500, relief="sunken", background="white")
        self.image_frame.place(x=500, y=15)
        self.img = None

        # MAIN LOOP
        self.window.mainloop()

    def loadImageProcessor(self, path):
        self.image_processor = ImageProcessor(path)

    def fileOpener(self):

        # open a file explorer
        # get the file name of the selected file by the user
        filename = filedialog.askopenfilename(initialdir="./", title="Select a File", filetypes=(
            ("JPG Files", "*.jpg"), ("JPEG Files", "*.jpeg"), ("PNG Files", "*.png")))

        # if the file open is succesful
        if filename:
            # We state that there's currently an opened file for the text editor
            self.image_path = filename
            self.loadImageProcessor(filename)
            self.displayImage()

    def countLight(self):
        pass

    def countDark(self):
        pass

    def displayImage(self):
        im = Image.fromarray(self.image_processor.display_img)
        self.img = ImageTk.PhotoImage(image=im)
        label = Label(self.image_frame, image=self.img)
        label.pack()
