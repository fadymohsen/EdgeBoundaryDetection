
import numpy as np
import cv2

class Chaincode():
    def __init__(self):
        self.chain_code = []
        
        # Define 8-connected neighbors
        self.neighbors = [(-1, -1), (0, -1), (1, -1), (1, 0),
                    (1, 1), (0, 1), (-1, 1), (-1, 0)]

    # Function to find the next boundary pixel
    def next_boundary_pixel(self,image, x, y, direction):
        height, width = image.shape
        for i in range(8):
            dx, dy = self.neighbors[(direction + i) % 8]
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < width and 0 <= new_y < height and image[new_y, new_x] != 0:
                return (new_x, new_y), (direction + i) % 8
        return None, None  # If no boundary pixel found within image bounds


    # # Function to generate chain code for the boundary
    # def generate_chain_code(self,contour):   
    #     if len(contour) > 0:
    #         x, y = contour[0][1], contour[0][0]  # Accessing the first point of the contour
    #         direction = 0  # Start with direction 0 (East)
    #         for point in contour[1:]:
    #             dx = point[1] - x
    #             dy = point[0] - y
                
    #             print("dx:", dx, "dy:", dy)  # Debugging
    #             x, y = point[1], point[0]
    #             print("x:", x, "y:", y)
    #             # Determine direction based on dx, dy
    #             if dx == 1 and dy == 0:
    #                 direction = 0
    #             elif dx == 1 and dy == -1:
    #                 direction = 1
    #             elif dx == 0 and dy == -1:
    #                 direction = 2
    #             elif dx == -1 and dy == -1:
    #                 direction = 3
    #             elif dx == -1 and dy == 0:
    #                 direction = 4
    #             elif dx == -1 and dy == 1:
    #                 direction = 5
    #             elif dx == 0 and dy == 1:
    #                 direction = 6
    #             elif dx == 1 and dy == 1:
    #                 direction = 7
    #             print("direction:", direction)
    #             self.chain_code.append(direction)
    #     return self.chain_code
  

    def generate_chain_code(self, contour):   
        if len(contour) > 0:
            x_prev, y_prev = contour[0][1], contour[0][0]  # Accessing the first point of the contour
            for point in contour[1:]:
                x, y = point[1], point[0]
                
                # Calculate angle between current and previous points
                angle = np.arctan2(y - y_prev, x - x_prev)
                
                # Convert angle to chain code
                direction = round(4 * angle / np.pi) % 8  # 8 directions
                
                self.chain_code.append(direction)
                
                # Update previous point
                x_prev, y_prev = x, y
                
        return self.chain_code

    def print_chain_code(self,contour):
        # Generate chain code
        self.chain_code = self.generate_chain_code(contour)
        print("Chain Code:", self.chain_code)
        # Convert chain code to symbols
        symbols = ['E', 'NE', 'N', 'NW', 'W', 'SW', 'S', 'SE']
        chain_code_symbols = [symbols[code] for code in self.chain_code]
        print("Chain Code Symbols:", chain_code_symbols)


