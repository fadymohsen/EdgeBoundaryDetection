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
            self.imageArray = cv2.rotate(imageArray, cv2.ROTATE_90_CLOCKWISE)
        edgeDetectedImage = self.cannyEdgeDetection(self.imageArray)
        selectedShape = self.ui.comboBox_houghDetectionMethod.currentText()
        if selectedShape == "Lines":
            self.detectLines(edgeDetectedImage)
        elif selectedShape == "Ellipse":
            self.detectEllipse(edgeDetectedImage)
        else:
            self.detectCircles(edgeDetectedImage, 10,15,radius=[50,5])

    def detectCircles(self, image, threshold,region,radius = None):
        # circles = cv2.HoughCircles(image,cv2.HOUGH_GRADIENT,1,20,
        #             param1=200,param2=30,minRadius=20,maxRadius=200)
        
        (M,N) = image.shape
        if radius == None:
            R_max = np.max((M,N))
            R_min = 3
        else:
            [R_max,R_min] = radius

        R = R_max - R_min
        #Initializing accumulator array.
        #Accumulator array is a 3 dimensional array with the dimensions representing
        #the radius, X coordinate and Y coordinate resectively.
        #Also appending a padding of 2 times R_max to overcome the problems of overflow
        A = np.zeros((R_max,M+2*R_max,N+2*R_max))
        B = np.zeros((R_max,M+2*R_max,N+2*R_max))

        #Precomputing all angles to increase the speed of the algorithm
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
                #Centering the blueprint circle over the edges
                #and updating the accumulator array
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