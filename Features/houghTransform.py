import numpy as np
import cv2
import pyqtgraph as pg
from pyqtgraph import ImageItem





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
            self.imageArray = cv2.rotate(imageArray, cv2.ROTATE_90_CLOCKWISE)
        edgeDetectedImage = self.cannyEdgeDetection(self.imageArray)
        selectedShape = self.ui.comboBox_houghDetectionMethod.currentText()
        if selectedShape == "Lines":
            lines, detected_image = self.detectLines(edgeDetectedImage)
            self.displayLines(detected_image, lines)
        elif selectedShape == "Ellipse":
            self.detectEllipse(edgeDetectedImage)
        else:
            self.detectCircles(edgeDetectedImage, 10,15,radius=[50,5])



    def detectCircles(self, image, threshold,region,radius = None):
        (M,N) = image.shape
        if radius == None:
            R_max = np.max((M,N))
            R_min = 3
        else:
            [R_max,R_min] = radius
        R = R_max - R_min
        A = np.zeros((R_max,M+2*R_max,N+2*R_max))
        B = np.zeros((R_max,M+2*R_max,N+2*R_max))
        theta = np.arange(0,360)*np.pi/180
        edges = np.argwhere(image[:,:])                                               #Extracting all edge coordinates
        for val in range(R):
            r = R_min+val
            #Creating a Circle Blueprint
            bprint = np.zeros((2*(r+1),2*(r+1)))
            (m,n) = (r+1,r+1)                                                       #Finding out the center of the blueprint
            for angle in theta:
                x = int(np.round(r*np.cos(angle)))
                y = int(np.round(r*np.sin(angle)))
                bprint[m+x,n+y] = 1
            constant = np.argwhere(bprint).shape[0]
            for x,y in edges:                                                       #For each edge coordinates
                X = [x-m+R_max,x+m+R_max]                                           #Computing the extreme X values
                Y= [y-n+R_max,y+n+R_max]                                            #Computing the extreme Y values
                A[r,X[0]:X[1],Y[0]:Y[1]] += bprint
            A[r][A[r]<threshold*constant/r] = 0

        for r,x,y in np.argwhere(A):
            temp = A[r-region:r+region,x-region:x+region,y-region:y+region]
            try:
                p,a,b = np.unravel_index(np.argmax(temp),temp.shape)
            except:
                continue
            B[r+(p-region),x+(a-region),y+(b-region)] = 1
        circles = B[:,R_max:-R_max,R_max:-R_max]
        image_with_circles = np.copy(self.imageArray)
        image_with_circles_color = cv2.cvtColor(image_with_circles, cv2.COLOR_GRAY2BGR)
        # Draw the circles as borders
        for r, x, y in np.argwhere(circles):
            cv2.circle(image_with_circles_color, (y, x), r, (0, 255, 0), 3)
        # Clear existing items in the appropriate view box
        self.ui.graphics_afterHoughDetection.clear()
        view_box = self.ui.graphics_afterHoughDetection.addViewBox()
        
        # Display the new image
        img_item = pg.ImageItem(image_with_circles_color)
        view_box.addItem(img_item)
    


    def detectLines(self, image):
        rho = 1
        theta = np.pi / 180
        threshold = 500
        min_line_len = 50
        max_line_gap = 30
        lines, detected_image = self.hough_transform(image, rho, theta, threshold, min_line_len, max_line_gap)
        return lines, detected_image



    def displayLines(self, image, lines):
        for line in lines:
            x0, y0, x1, y1 = line
            cv2.line(image, (int(x0), int(y0)), (int(x1), int(y1)), (0, 0, 255), 2)
        # Display the image with detected lines
        self.displayImage(image)




    def displayImage(self, image):
        # Assuming you have QGraphicsView or similar for displaying images
        self.ui.graphics_afterHoughDetection.clear()
        # Create a PlotItem or ViewBox
        view_box = self.ui.graphics_afterHoughDetection.addViewBox()
        # Create an ImageItem and add it to the ViewBox
        image_item = ImageItem(image)
        view_box.addItem(image_item)

        


    def hough_transform(self, img, rho, theta, threshold, min_line_len=30, max_line_gap=50):
        height, width = img.shape
        diag_len = np.ceil(np.sqrt(height * height + width * width))
        rho_bins = np.int32(diag_len / rho)
        theta_bins = np.int32(np.pi / theta)
        accumulator = np.zeros((rho_bins, theta_bins), dtype=np.uint8)
        y, x = np.nonzero(img)
        num_edge_points = len(x)
        for i in range(num_edge_points):
            for theta_index in range(theta_bins):

                rho_val = x[i] * np.cos(theta_index * theta) + y[i] * np.sin(theta_index * theta)

                rho_index = np.int32(rho_val / rho)
                # increment the accumulator
                accumulator[rho_index, theta_index] += 1
        # get the indices of the accumulator where the values are greater than the threshold
        indices = np.nonzero(accumulator >= threshold)
        # get the number of lines
        num_lines = len(indices[0])
        # create an array to store the lines
        lines = []
        # get the lines
        for i in range(num_lines):
            
            rho_index = indices[0][i]
            theta_index = indices[1][i]
            # get the rho and theta values
            rho_val = rho_index * rho
            theta_val = theta_index * theta
            # get the x and y values
            x0 = np.cos(theta_val) * rho_val
            y0 = np.sin(theta_val) * rho_val
            x1 = int(x0 + diag_len * np.cos(theta_val + np.pi / 2))
            y1 = int(y0 + diag_len * np.sin(theta_val + np.pi / 2))
            # use minLineLength and maxLineGap to filter out the lines
            if np.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2) > min_line_len and np.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2) > max_line_gap:
                lines.append([x0, y0, x1, y1])
        return lines, img






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