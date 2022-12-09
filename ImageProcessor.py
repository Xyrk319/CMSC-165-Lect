import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


class ImageProcessor():

    def __init__(self, path):

        # image path
        self.PATH = path

        # Holder for the counts of pollen
        self.count_dark_polen = None
        self.count_light_polen = None

        # load image
        self.img = cv.imread(self.PATH)

        # this image can be used to display in the GUI
        self.display_img = self.img.copy()

        # rescale the image so that the masks will be able to accomodate different sizes
        scale = 1/(self.img.shape[1] / 1000)
        self.img = cv.resize(self.img, (0, 0), fx=scale, fy=scale)

        # an image copy for the clean background version
        self.clean_background_img = None

        # holder for the image of the pollens
        self.dark_pollens = None
        self.light_pollens = None

        # MAIN PROCESS
        self.run()

    def run(self):

        # clean the background of the image so that the remaining colors will be the two pollens
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

        # create a gray image copy
        colored_image = self.img.copy()
        gray_image = cv.cvtColor(colored_image, cv.COLOR_BGR2GRAY)

        # OTSU Threshold which properly separates the foreground from the background
        _, img = cv.threshold(
            gray_image, 55, 255, cv.THRESH_OTSU)

        # invert the mask
        inverted_mask = cv.bitwise_not(img)

        # retain the pollens in the image
        result = cv.bitwise_and(
            colored_image, colored_image, mask=inverted_mask)

        # convert the black pixels to white
        self.changePixelsBlackToWhite(result)

        self.clean_background_img = result

    def pseudoColoring(self):

        # convert to HSV for easier detection of the color range
        img = self.clean_background_img.copy()
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

        # dark pollen - hue for the dark pinkish violet is from 120-170
        lower_dark = np.array([120, 0, 0])
        upper_dark = np.array([170, 255, 255])

        # dark pollen mask
        mask = cv.inRange(hsv, lower_dark, upper_dark)

        # Get the dark pollens only
        dark_result = cv.bitwise_and(self.clean_background_img,
                                     self.clean_background_img, mask=mask)

        # light pollen mask
        inverted_mask = cv.bitwise_not(mask)

        # get the light pollens only
        light_result = cv.bitwise_and(self.clean_background_img,
                                      self.clean_background_img, mask=inverted_mask)

        # fix the black pixels, standardize all of the background to white
        self.changePixelsBlackToWhite(dark_result)
        self.changePixelsBlackToWhite(light_result)

        # remove noises on black using mean filter mask
        noiseless_dark_result = cv.fastNlMeansDenoisingColored(
            dark_result, None, 20, 20, 11, 31)

        # create a struct width for the binary morphology for the light pollen
        # this is to remove the border of the dark pollens that were left from the inverted mask
        struct_width = cv.getStructuringElement(cv.MORPH_CROSS, (2, 3))
        light_result = cv.dilate(light_result, struct_width,
                                 iterations=2)
        noiseless_light_result = cv.fastNlMeansDenoisingColored(
            light_result, None, 20, 20, 11, 31)

        # results
        self.dark_pollens = noiseless_dark_result

        self.light_pollens = noiseless_light_result

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

    # will count the number of objects within an image
    def countObjects(self, image, label):

        img = image.copy()
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        # blurring the image
        # Note: this removes some light pollens hence it is currently commented out
        # blur = cv.GaussianBlur(img, (11, 11), 0)

        # canny edge detection
        canny = cv.Canny(img, 30, 150, 3)

        # binary dilation
        dilated = cv.dilate(canny, (1, 1), iterations=2)
        contours, hierarchy = cv.findContours(
            dilated.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
        # check the contours detected
        # rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        # contour_img = cv.drawContours(rgb, contours, -1, (0, 255, 0), 2)
        # self.showImage(contour_img)

        print(f'Number of {label} Pollens', len(contours))
