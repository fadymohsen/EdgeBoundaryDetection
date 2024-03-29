import cv2
import numpy as np
import matplotlib.pyplot as plt






class ActiveContour:
    def __init__(self, image_path):
        self.image_path = image_path
        self.gray_image, self.edge_image = self.load_and_process_image()



    def load_and_process_image(self):
        image = cv2.imread(self.image_path, cv2.IMREAD_COLOR)  # Use color mode to load to ensure it can be rotated correctly
        
        if image is None:
            print(f"Failed to load image from {self.image_path}")
            return None, None
        
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        print("\nSUCCESS - Image is converted to GreyScale")

        rotated_image = np.rot90(gray_image, -1)  # Rotate 90 degrees counter-clockwise
        print("SUCCESS - Image is Rotated by 90 Degrees")
        
        edge_image = cv2.Canny(rotated_image, 30, 150)
        print("SUCCESS - Image is converted to Canny Edges\n\n")
        
        return rotated_image, edge_image




    def get_gray_image_data(self):
        return self.gray_image

    def get_edge_image_data(self):
        return self.edge_image
