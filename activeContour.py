import cv2
import numpy as np
import matplotlib.pyplot as plt






class ActiveContour:
    def __init__(self, image_path):
        self.image_path = image_path
        self.gray_image, self.edge_image = self.load_and_process_image()



    def load_and_process_image(self):
        if self is None:
            print(f"Failed to load image from {self.image_path}")
            return None, None
        
        gray_image = cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)
        print("\nSUCCESS - Image is converted to GreyScale")
        edge_image = cv2.Canny(gray_image, 30, 150)
        print("SUCCESS - Image is converted to Canny Edges\n\n")
        return gray_image, edge_image



    def get_gray_image_data(self):
        return self.gray_image

    def get_edge_image_data(self):
        return self.edge_image
