import cv2 as cv
import numpy as np


class ImageProcessor():

    def __init__(self, path, ):
        self.PATH = path

        self.count_dark_polen = None
        self.count_light_polen = None

        # load image
        self.img = cv.imread(self.PATH)

        # this image can be used to display in the GUI
        self.display_img = self.img.copy()

        # resizing the image
        scale_percentage = 70
        width = int(self.display_img.shape[1] * scale_percentage/100)
        height = int(self.display_img.shape[0] * scale_percentage/100)
        self.display_img = cv.resize(self.display_img, (width, height),
                                     interpolation=cv.INTER_AREA)
        # convert it to RGB
        blue, green, red = cv.split(self.display_img)
        self.display_img = cv.merge((red, green, blue))

        # self.binary_image = self.binarize()

        # self.showImage(self.binary_image, self.img.shape[0], self.img.shape[1])

    def showImage(self, img, height, width):

        image = img.copy()
        cv.resize(image, (height, width))

        cv.imshow('Image', image)
        #  wait any key, parameter is seconds if 0 then infinite.
        cv.waitKey(0)
        # destroy all windows created
        cv.destroyAllWindows()

    def binarize(self):

        # hsv = cv.cvtColor(self.img, cv.COLOR_BGR2HSV)
        lower_range = np.array([105, 100, 108])
        upper_range = np.array([110, 130, 255])

        mask = cv.inRange(self.img, lower_range, upper_range)

        return mask
