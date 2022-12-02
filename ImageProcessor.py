import cv2 as cv
import numpy as np


class ImageProcessor():

    def __init__(self, path, ):
        PATH = path

        # load image
        img = cv.imread(PATH)

    def showImage(self, height, width):

        image = self.img.copy()
        cv.resize(image, (height, width))

        cv.imshow('Image', image)
        #  wait any key, parameter is seconds if 0 then infinite.
        cv.waitKey(0)
        # destroy all windows created
        cv.destroyAllWindows()
