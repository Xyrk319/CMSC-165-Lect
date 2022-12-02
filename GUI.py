from tkinter import filedialog
from tkinter import tk
import ImageProcessor


class GUI:

    def __init__(self):

        # attributes here
        self.window = tk()
        self.window.title("CMSC 165 - Lecture Project")
        self.window.geometry("700x600")

        # MAIN LOOP
        self.window.mainloop()

        self.imageProcessor = None
