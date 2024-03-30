# #chain code with the visualization on matplotlib
# import numpy as np
# import matplotlib.pyplot as plt
# import cv2

# # Define 8-connected neighbors
# neighbors = [(-1, -1), (0, -1), (1, -1), (1, 0),
#              (1, 1), (0, 1), (-1, 1), (-1, 0)]

# # Function to find the next boundary pixel
# def next_boundary_pixel(image, x, y, direction):
#     height, width = image.shape
#     for i in range(8):
#         dx, dy = neighbors[(direction + i) % 8]
#         new_x, new_y = x + dx, y + dy
#         if 0 <= new_x < width and 0 <= new_y < height and image[new_y, new_x] != 0:
#             return (new_x, new_y), (direction + i) % 8
#     return None, None  # If no boundary pixel found within image bounds


# # Function to generate chain code for the boundary
# def generate_chain_code(contour):
#     chain_code = []
#     if len(contour) > 0:
#         x, y = contour[0][0][0], contour[0][0][1]  # Accessing the first point of the contour
#         direction = 0  # Start with direction 0 (East)
#         for point in contour[1:]:
#             dx = point[0][0] - x
#             dy = point[0][1] - y
#             x, y = point[0][0], point[0][1]
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
#             chain_code.append(direction)
#     return chain_code

# # Load your own image
# image_path = r"C:\Users\hp\Downloads\WhatsApp Image 2024-03-29 at 4.02.13 PM.jpeg"  # Replace 'your_image.jpg' with your image file path
# image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
# # C:\Users\hp\Downloads\WhatsApp Image 2024-03-29 at 4.02.13 PM.jpeg-->apple photo
# #C:\Users\hp\Desktop\CV2\EdgeBoundaryDetection\Images\pikachu-u11.jpg --> pockimon photo
# # C:\Users\hp\Desktop\CV2\EdgeBoundaryDetection\Images\Spongebob-cartoon-1024x848.png-->sponge bob
# #  C:\Users\hp\Desktop\CV2\EdgeBoundaryDetection\Images\hot-cartoons-8-435-1a28836186f448749f53127465d172a0.jpg-->damo impossible
# # C:\Users\hp\Desktop\CV2\EdgeBoundaryDetection\Images\lena.png -->lena png

# # Apply active contour model to detect contour
# snake = cv2.imread(image_path, 0)
# snake = cv2.GaussianBlur(snake, (3, 3), 0)
# snake = cv2.Canny(snake, 100, 200)
# contours, _ = cv2.findContours(snake, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# if contours:
#     contour = max(contours, key=cv2.contourArea)  # Select the largest contour

#     # Generate chain code
#     chain_code = generate_chain_code(contour)
#     print("Chain Code:", chain_code)

#     # Convert chain code to symbols
#     symbols = ['E', 'NE', 'N', 'NW', 'W', 'SW', 'S', 'SE']
#     chain_code_symbols = [symbols[code] for code in chain_code]
#     print("Chain Code Symbols:", chain_code_symbols)

#     # Plot chain code symbols on image
#     plt.subplot(1, 2, 1)
#     plt.imshow(image, cmap='gray')
#     plt.title('Original Image')
#     plt.xticks([]), plt.yticks([])

#     plt.subplot(1, 2, 2)
#     plt.plot(contour[:, 0, 0], contour[:, 0, 1], 'r')
#     plt.title('Detected Contour with Chain Code')
#     plt.xticks([]), plt.yticks([])

#     plt.show()
# else:
#     print("No contours found.")

# -----------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------


#chain code only

import numpy as np
import cv2

# Define 8-connected neighbors
neighbors = [(-1, -1), (0, -1), (1, -1), (1, 0),
             (1, 1), (0, 1), (-1, 1), (-1, 0)]

# Function to find the next boundary pixel
def next_boundary_pixel(image, x, y, direction):
    height, width = image.shape
    for i in range(8):
        dx, dy = neighbors[(direction + i) % 8]
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < width and 0 <= new_y < height and image[new_y, new_x] != 0:
            return (new_x, new_y), (direction + i) % 8
    return None, None  # If no boundary pixel found within image bounds


# Function to generate chain code for the boundary
def generate_chain_code(contour):
    chain_code = []
    if len(contour) > 0:
        x, y = contour[0][0][0], contour[0][0][1]  # Accessing the first point of the contour
        direction = 0  # Start with direction 0 (East)
        for point in contour[1:]:
            dx = point[0][0] - x
            dy = point[0][1] - y
            x, y = point[0][0], point[0][1]
            # Determine direction based on dx, dy
            if dx == 1 and dy == 0:
                direction = 0
            elif dx == 1 and dy == -1:
                direction = 1
            elif dx == 0 and dy == -1:
                direction = 2
            elif dx == -1 and dy == -1:
                direction = 3
            elif dx == -1 and dy == 0:
                direction = 4
            elif dx == -1 and dy == 1:
                direction = 5
            elif dx == 0 and dy == 1:
                direction = 6
            elif dx == 1 and dy == 1:
                direction = 7
            chain_code.append(direction)
    return chain_code

# Load your own image
image_path = r"C:\Users\hp\Downloads\WhatsApp Image 2024-03-29 at 4.02.13 PM.jpeg"  # Replace 'your_image.jpg' with your image file path
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Apply active contour model to detect contour
snake = cv2.imread(image_path, 0)
snake = cv2.GaussianBlur(snake, (3, 3), 0)
snake = cv2.Canny(snake, 100, 200)
contours, _ = cv2.findContours(snake, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
if contours:
    contour = max(contours, key=cv2.contourArea)  # Select the largest contour

    # Generate chain code
    chain_code = generate_chain_code(contour)
    print("Chain Code:", chain_code)

    # Convert chain code to symbols
    symbols = ['E', 'NE', 'N', 'NW', 'W', 'SW', 'S', 'SE']
    chain_code_symbols = [symbols[code] for code in chain_code]
    print("Chain Code Symbols:", chain_code_symbols)

else:
    print("No contours found.")

