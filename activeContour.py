import cv2
import numpy as np





class ActiveContour:
    def __init__(self, image_path):
        self.image_path = image_path
        self.gray_image, self.edge_image = self.load_and_process_image()

    def load_and_process_image(self):
        """Loads the image, converts it to grayscale, and applies Canny edge detection."""
        gray_image = cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)
        if gray_image is None:
            print(f"Failed to load image from {self.image_path}")
            return None, None
        
        edge_image = cv2.Canny(gray_image, 30, 150)
        print("\n\nImage loaded and processed\n\n")
        return gray_image, edge_image

    def get_gray_image_data(self):
        """Returns the grayscale image data."""
        return self.gray_image

    def get_edge_image_data(self):
        """Returns the Canny edge processed image data."""
        return self.edge_image
