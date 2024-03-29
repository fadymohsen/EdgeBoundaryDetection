import cv2
import numpy as np
import sys
from scipy import ndimage
from scipy.interpolate import RectBivariateSpline
from skimage.segmentation import active_contour
from skimage.filters import gaussian
import matplotlib.pyplot as plt


def getImage():
    filename = 'Images/ActiveContour-Valid-1.jpg'
    image = cv2.imread(filename)
    return image


def showImg(img, contours=None, winName='Image'):
    disp_img = img.copy()
    disp_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if contours is not None:
        # cv2.polylines(disp_img, np.int32([contours]), isClosed=True, color=(0, 255, 0))
        # cv2.imshow(winName, disp_img)
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.imshow(disp_img, cmap=plt.cm.gray)
        ax.plot(init[:, 0], init[:, 1], '--r', lw=3)
        ax.plot(contours[:, 0], contours[:, 1], '-b', lw=3)
        ax.set_xticks([]), ax.set_yticks([])
        ax.axis([0, img.shape[1], img.shape[0], 0])
        plt.show()

    else:
        cv2.imshow(winName, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


orig_image = getImage()
img = orig_image


def nothing(x):
    pass


def centre_x(x):
    y = cv2.getTrackbarPos("Centre_y", "Image")
    r = cv2.getTrackbarPos("Radius", "Image")
    new_img = orig_image.copy()
    cv2.drawMarker(new_img, (x, y), color=(0, 0, 255), markerType=1, markerSize=10)
    cv2.circle(new_img, (x, y), r, color=(0, 0, 255), thickness=2, lineType=1)
    cv2.imshow("Image", new_img)


def centre_y(y):
    x = cv2.getTrackbarPos("Centre_x", "Image")
    r = cv2.getTrackbarPos("Radius", "Image")
    new_img = orig_image.copy()
    cv2.drawMarker(new_img, (x, y), color=(0, 0, 255), markerType=1, markerSize=10)
    cv2.circle(new_img, (x, y), r, color=(0, 0, 255), thickness=2, lineType=1)
    cv2.imshow("Image", new_img)


def radius(r):
    x = cv2.getTrackbarPos("Centre_x", "Image")
    y = cv2.getTrackbarPos("Centre_y", "Image")
    new_img = orig_image.copy()
    cv2.drawMarker(new_img, (x, y), color=(0, 0, 255), markerType=1, markerSize=10)
    cv2.circle(new_img, (x, y), r, color=(0, 0, 255), thickness=2, lineType=1)
    cv2.imshow("Image", new_img)


cv2.namedWindow("Image")
cv2.imshow("Image", orig_image)
cv2.createTrackbar("Iterations", "Image", 100, 10000, nothing)
cv2.createTrackbar("Centre_x", "Image", int(img.shape[0]/2), int(img.shape[0]), centre_x)
cv2.createTrackbar("Centre_y", "Image", int(img.shape[1]/2), int(img.shape[1]), centre_y)
cv2.createTrackbar("Radius", "Image", int(img.shape[0]/4), int(img.shape[0]/2), radius)
cv2.createTrackbar("Alpha *0.01", "Image", 1, 100, nothing)
cv2.createTrackbar("Beta *0.01", "Image", 1, 100, nothing)
cv2.createTrackbar("Gamma *0.01", "Image", 1, 100, nothing)
cv2.createTrackbar("Fraction convergence * 0.01", "Image", 10, 100, nothing)
cv2.createTrackbar("Time Delay (ms)", "Image", 1, 100, nothing)
cv2.createTrackbar("Ready", "Image", 0, 1, nothing)
# cv2.destroyAllWindows()
while True:
    k = cv2.waitKey(0)
    if k == ord('q'):
        break
    start = cv2.getTrackbarPos("Ready", "Image")
    if not start:
        pass
    else:
        img = orig_image.copy()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = gaussian(img, 3)
        cv2.setTrackbarPos("Ready", "Image", 0)
        centre_x = cv2.getTrackbarPos("Centre_x", "Image")
        centre_y = cv2.getTrackbarPos("Centre_y", "Image")
        radius = cv2.getTrackbarPos("Radius", "Image")
        alpha = cv2.getTrackbarPos("Alpha *0.01", "Image") * 0.01
        beta = cv2.getTrackbarPos("Beta *0.01", "Image") * 0.01
        gamma = cv2.getTrackbarPos("Gamma *0.01", "Image") * 0.01
        frac_cvg = cv2.getTrackbarPos("Fraction convergence * 0.01", "Image") * 0.01
        td = cv2.getTrackbarPos("Time Delay (ms)", "Image")

        s = np.linspace(0, 2*np.pi, 1000)
        r = centre_y + radius * np.sin(s)
        c = centre_x + radius * np.cos(s)

        init = np.array([c, r]).T
        contours = init
        max_iterations = cv2.getTrackbarPos("Iterations", "Image")
        iteration = max_iterations
        while iteration > 0:
            cv2.namedWindow("iterations")
            cv2.imshow("iterations", img)
            img1 = img.copy()
            contours = active_contour(img, contours, alpha=alpha, beta=beta, gamma=gamma, convergence=frac_cvg, max_iterations=10)
            cv2.polylines(img1, np.int32([contours]), isClosed=True, color=0)
            text = cv2.putText(img1, f"Iteration: {max_iterations - iteration}", (20, 20), fontFace=1, fontScale=1, color=0)

            cv2.imshow("iterations", img1)
            k = cv2.waitKey(td)
            if k == ord('q'):
                break
            iteration -= 10

        cv2.destroyWindow("iterations")

        showImg(orig_image, contours, "Image")
        # k = cv2.waitKey(0)
        # if k == ord('q'):
        #     break

cv2.destroyAllWindows()