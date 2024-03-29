import cv2
import numpy as np





class ActiveContour:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = self.load_and_process_image()



    def load_and_process_image(self):
        """Loads the image from the specified path and converts it to grayscale."""
        image = cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            print(f"Failed to load image from {self.image_path}")
            return None
        else:
            # Here, you can apply additional image processing as needed
            print("\n\nImage loaded and processed\n\n")
            return image



    def get_image_data(self):
        """Returns the processed image data."""
        return self.image
