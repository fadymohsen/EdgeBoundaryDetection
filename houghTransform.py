import numpy as np
import cv2
import pyqtgraph as pg

class houghTransformShapeDetection:
    def __init__(self, main_tab_widget):
        self.main_tab_widget = main_tab_widget
        self.ui = self.main_tab_widget
        self.ui.comboBox_houghDetectionMethod.activated.connect(self.detectShape)

    def detectShape(self):
        if self.main_tab_widget.selected_image_path:
            imageArray = cv2.imread(self.main_tab_widget.selected_image_path)
            if imageArray.ndim == 3:
                imageArray = cv2.cvtColor(imageArray, cv2.COLOR_BGR2GRAY)
            imageArray = cv2.rotate(imageArray, cv2.ROTATE_90_CLOCKWISE)
        edgeDetectedImage = self.cannyEdgeDetection(imageArray)
        selectedShape = self.ui.comboBox_houghDetectionMethod.currentText()
        if selectedShape == "Lines":
            self.detectLines(edgeDetectedImage)
        elif selectedShape == "Ellipse":
            self.detectEllipse(edgeDetectedImage)
        else:
            self.detectCircles(edgeDetectedImage)

    def detectCircles(self, image):
        pass
    
    def detectLines(self, image):
        pass

    def detectEllipse(self, image):
        pass

    def cannyEdgeDetection(self, image):
        blurred_img = cv2.GaussianBlur(image, (5, 5), 4)

        sobelFilterVertical = np.array([[-1, 0, 1],
                                        [-2, 0, 2],
                                        [-1, 0, 1]])

        sobelFilterHorizontal = np.array([[-1, -2, -1],
                                            [0, 0, 0],
                                            [1, 2, 1]])

        Gradient_x = cv2.filter2D(blurred_img, -1, sobelFilterVertical) 
        Gradient_y = cv2.filter2D(blurred_img, -1, sobelFilterHorizontal) 

        Gradient = np.hypot(Gradient_x, Gradient_y)
        Gradient = Gradient / Gradient.max() * 255
        angle = np.arctan2(Gradient_y, Gradient_x)

        M, N = Gradient.shape
        Z = np.zeros((M, N), dtype=np.int32)
        angle = angle * 180 / np.pi
        angle[angle < 0] += 180

        for i in range(1, M - 1):
            for j in range(1, N - 1):
                q = 255
                r = 255
                if (0 <= angle[i, j] < 22.5) or (157.5 <= angle[i, j] <= 180):
                    r = Gradient[i, j - 1]
                    q = Gradient[i, j + 1]
                elif (22.5 <= angle[i, j] < 67.5):
                    r = Gradient[i - 1, j + 1]
                    q = Gradient[i + 1, j - 1]
                elif (67.5 <= angle[i, j] < 112.5):
                    r = Gradient[i - 1, j]
                    q = Gradient[i + 1, j]
                elif (112.5 <= angle[i, j] < 157.5):
                    r = Gradient[i + 1, j + 1]
                    q = Gradient[i - 1, j - 1]

                if (Gradient[i, j] >= q) and (Gradient[i, j] >= r):
                    Z[i, j] = Gradient[i, j]
                else:
                    Z[i, j] = 0
        thinEdgesImage = Z

        lowThresholdRatio = 0.05
        highThresholdRatio = 0.09
        highThreshold = thinEdgesImage.max() * highThresholdRatio
        lowThreshold = highThreshold * lowThresholdRatio
        M, N = Z.shape
        thresholdedImage = np.zeros((M, N), dtype=np.int32)
        weak = 153
        strong = 255

        strong_i, strong_j = np.where(thinEdgesImage >= highThreshold)
        weak_i, weak_j = np.where((thinEdgesImage <= highThreshold) & (thinEdgesImage >= lowThreshold))
        thresholdedImage[strong_i, strong_j] = strong
        thresholdedImage[weak_i, weak_j] = weak

        for i in range(1, M - 1):
            for j in range(1, N - 1):
                if thresholdedImage[i, j] == weak:
                    if (
                        (thresholdedImage[i + 1, j - 1] == strong) or (thresholdedImage[i + 1, j] == strong) or
                        (thresholdedImage[i + 1, j + 1] == strong) or (thresholdedImage[i, j - 1] == strong) or
                        (thresholdedImage[i, j + 1] == strong) or (thresholdedImage[i - 1, j - 1] == strong) or
                        (thresholdedImage[i - 1, j] == strong) or (thresholdedImage[i - 1, j + 1] == strong)
                    ):
                        thresholdedImage[i, j] = strong
                    else:
                        thresholdedImage[i, j] = 0
        return thresholdedImage