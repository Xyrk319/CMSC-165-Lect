import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


class ImageProcessor():

    def __init__(self, path):
        self.PATH = path

        self.k = 3

        # Holder for the counts of pollen
        self.count_dark_polen = None
        self.count_light_polen = None

        # load image
        self.img = cv.imread(self.PATH)

        # this image can be used to display in the GUI

        self.display_img = self.img.copy()

        scale = 1/(self.img.shape[1] / 1000)
        self.img = cv.resize(self.img, (0, 0), fx=scale, fy=scale)

        # self.countObjects(self.img, 'All')
        self.clean_background_img = None

        # holder for the image of the pollens
        self.dark_pollens = None
        self.light_pollens = None

        self.cleanBackground()

        self.pseudoColoring()

        self.countObjects(self.dark_pollens, 'Dark')
        self.countObjects(self.light_pollens, 'Light')

    def showImage(self, img):

        image = img.copy()
        cv.imshow('Image', image)
        #  wait any key, parameter is seconds if 0 then infinite.
        cv.waitKey(0)
        # destroy all windows created
        cv.destroyAllWindows()

    def binarize(self):

        # hsv = cv.cvtColor(self.img, cv.COLOR_BGR2HSV)
        lower_range = np.array([0, 0, 0])
        upper_range = np.array([0, 0, 255])

        mask = cv.inRange(self.hsv_image, lower_range, upper_range)

        return mask

    # returns a white background

    def cleanBackground(self):

        colored_image = self.img.copy()
        gray_image = cv.cvtColor(colored_image, cv.COLOR_BGR2GRAY)

        # OTSU Threshold which properly separates the foreground from the background
        _, img = cv.threshold(
            gray_image, 55, 255, cv.THRESH_OTSU)

        inverted_mask = cv.bitwise_not(img)

        result = cv.bitwise_and(
            colored_image, colored_image, mask=inverted_mask)

        # convert the black pixels to white
        self.changePixelsBlackToWhite(result)

        self.clean_background_img = result

    def pseudoColoring(self):
        img = self.clean_background_img.copy()
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

        # dark pollen
        lower_dark = np.array([120, 0, 0])
        upper_dark = np.array([170, 255, 255])

        mask = cv.inRange(hsv, lower_dark, upper_dark)

        dark_result = cv.bitwise_and(self.clean_background_img,
                                     self.clean_background_img, mask=mask)

        inverted_mask = cv.bitwise_not(mask)

        light_result = cv.bitwise_and(self.clean_background_img,
                                      self.clean_background_img, mask=inverted_mask)

        self.changePixelsBlackToWhite(dark_result)
        self.changePixelsBlackToWhite(light_result)
        # self.changePixelsColoredToBlack(dark_result)
        # self.changePixelsColoredToBlack(light_result)

        # denoising
        noiseless_dark_result = cv.fastNlMeansDenoisingColored(
            dark_result, None, 20, 20, 11, 31)

        # filter mask
        struct_width = cv.getStructuringElement(cv.MORPH_CROSS, (2, 3))
        light_result = cv.dilate(light_result, struct_width,
                                 iterations=2)
        noiseless_light_result = cv.fastNlMeansDenoisingColored(
            light_result, None, 20, 20, 11, 31)

        self.dark_pollens = noiseless_dark_result

        self.light_pollens = noiseless_light_result
        # self.showImage(self.light_pollens)

    def changePixelsBlackToWhite(self, img):
        black_pixels = np.where(
            (img[:, :, 0] == 0) &
            (img[:, :, 1] == 0) &
            (img[:, :, 2] == 0)
        )

        # set those pixels to white
        img[black_pixels] = [255, 255, 255]

    def changePixelsColoredToBlack(self, img):
        black_pixels = np.where(
            (img[:, :, 0] != 0) &
            (img[:, :, 1] != 0) &
            (img[:, :, 2] != 0)
        )

        # set those pixels to white
        img[black_pixels] = [0, 0, 0]

    def countObjects(self, image, label):

        img = image.copy()
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        # blurring the image
        # blur = cv.GaussianBlur(img, (11, 11), 0)
        # self.showImage(blur)

        # canny edge detection
        canny = cv.Canny(img, 30, 150, 3)

        # binary dilation
        dilated = cv.dilate(canny, (1, 1), iterations=2)
        contours, hierarchy = cv.findContours(
            dilated.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
        # rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        # contour_img = cv.drawContours(rgb, contours, -1, (0, 255, 0), 2)

        # self.showImage(contour_img)

        print(f'Number of {label} Pollens', len(contours))
