import cv2
import matplotlib.pyplot as plt
import numpy as np

def calculate_direction(curr_point, next_point):
    # Calculate relative positions
    delta_row = next_point[0] - curr_point[0]
    delta_col = next_point[1] - curr_point[1]
    
    # Determine direction based on relative positions
    if delta_row == 0:
        if delta_col == 1:
            return 0  # East
        elif delta_col == -1:
            return 4  # West
    elif delta_row == 1:
        if delta_col == 1:
            return 1  # Northeast
        elif delta_col == 0:
            return 2  # North
        elif delta_col == -1:
            return 3  # Northwest
    elif delta_row == -1:
        if delta_col == 1:
            return 7  # Southeast
        elif delta_col == 0:
            return 6  # South
        elif delta_col == -1:
            return 5  # Southwest


def generate_chain_code(contour_points):
    chain_code = []
    for i in range(len(contour_points)):
        curr_point = contour_points[i]
        next_point = contour_points[(i + 1) % len(contour_points)]  # Wrap around for last point
        direction = calculate_direction(curr_point, next_point)
        chain_code.append(direction)
    return chain_code


def plot_chain_code(chain_code):
    # Initialize the figure
    plt.figure(figsize=(8, 8))
    ax = plt.gca()
    ax.set_aspect('equal')

    # Define arrow directions
    directions = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
    arrow_length = 0.8

    # Plot arrows for each direction in the chain code
    current_position = np.array([0, 0])
    for code in chain_code:
        if code is not None:  # Ignore None values
            direction = directions[code]
            next_position = current_position + np.array(direction) * arrow_length
            arrow = plt.arrow(current_position[0], current_position[1], direction[0], direction[1], head_width=0.1, head_length=0.2, fc='blue', ec='blue')
            ax.add_patch(arrow)
            current_position = next_position

    # Set plot limits
    ax.set_xlim(-150, 150)
    ax.set_ylim(-150, 150)
    ax.set_title('Chain Code')
    ax.set_aspect('equal', adjustable='box')
    plt.show()



##static hta soghayra
# def plot_chain_code(chain_code):
#     # Create a blank image to draw arrows on
#     img = np.zeros((500, 500, 3), dtype=np.uint8)
#     img.fill(255)  # Fill image with white color

#     # Define arrow directions
#     directions = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
#     arrow_length = 20  # Length of each arrow

#     # Starting position for drawing arrows
#     current_position = (250, 250)

#     # Draw arrows for each direction in the chain code
#     for code in chain_code:
#         if code is not None:  # Ignore None values
#             direction = directions[code]
#             next_position = (current_position[0] + direction[0] * arrow_length, current_position[1] + direction[1] * arrow_length)
#             cv2.arrowedLine(img, current_position, next_position, (0, 0, 255), thickness=2)
#             current_position = next_position

#     # Display the image with arrows
#     cv2.imshow('Chain Code', img)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

# Load the image
image = cv2.imread(r"C:\Users\hp\Downloads\b3ccef2eda2ee85ba89ce3f8d3e69205.jpg", cv2.IMREAD_GRAYSCALE)
#C:\Users\hp\Downloads\WhatsApp Image 2024-03-29 at 4.02.13 PM.jpeg   --> apple photo
#C:\Users\hp\Downloads\b3ccef2eda2ee85ba89ce3f8d3e69205.jpg   ---> lama photo
#C:\Users\hp\Downloads\FreemanCode1.png  --> sora 3ndi eli gahza

# Apply Canny edge detection
edges = cv2.Canny(image, 100, 200)

# Find contours
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contour_points = contours[0].reshape(-1, 2)

# Generate chain code
chain_code = generate_chain_code(contour_points)
print("Chain Code:", chain_code)

# Plot chain code
plot_chain_code(chain_code)
