import numpy as np
import cv2
from skimage import data

class ContourOptimizer:
    def __init__(self, image_path):
        self.image = cv2.imread(image_path, 1)
        if self.image is None:
            raise FileNotFoundError("Image file not found.")
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.image = np.pad(self.image, pad_width=30, mode='constant', constant_values=255)
        self.edge_image = cv2.Canny(self.image, 30, 150)
        self.contour_points = []

    def norm_0_1(self, arr):    
        maximum = np.amax(arr)
        return arr / maximum if maximum else arr

    def draw_point(self, lap, row, col, val=0, w1=6, w2=4):
        lap[row - w1 // 2:row + w1 // 2 + 1, col - w2 // 2:col + w2 // 2 + 1] = val
        lap[row - w2 // 2:row + w2 // 2 + 1, col - w1 // 2:col + w1 // 2 + 1] = val
        return lap

    def draw_contour(self, lap, contour_points, val=255):
        for i in range(len(contour_points)):
            lap = self.draw_point(lap, contour_points[i][0], contour_points[i][1], val)
            cv2.line(lap,
                     (contour_points[i][1], contour_points[i][0]),
                     (contour_points[(i + 1) % len(contour_points)][1], contour_points[(i + 1) % len(contour_points)][0]),
                     val, 1)
        return lap

    def calc_elastic_energy(self, alpha, row, col, next_point):
        elastic_energy = np.zeros((7, 7), np.float32)
        for i in range(-3, 4):
            for j in range(-3, 4):
                elastic_energy[i + 3, j + 3] = alpha * (np.square(next_point[0] - (row + i)) + np.square(next_point[1] - (col + j)))
        return self.norm_0_1(elastic_energy)

    def calc_smooth_energy(self, beta, row, col, next_point, prior_point):
        smooth_energy = np.zeros((7, 7), np.float32)
        for i in range(-3, 4):
            for j in range(-3, 4):
                smooth_energy[i + 3, j + 3] = beta * (np.square(next_point[0] - (2 * (row + i)) + prior_point[0]) + np.square(next_point[1] - (2 * (col + j)) + prior_point[1]))
        return self.norm_0_1(smooth_energy)

    def calc_external_energy(self, gamma, row, col):
        external_energy = np.zeros((7, 7), np.float32)
        for i in range(-3, 4):
            for j in range(-3, 4):
                external_energy[i + 3, j + 3] = gamma * np.square(self.edge_image[row + i, col + j])
        return 1 - self.norm_0_1(external_energy)

    def sum_energies(self, e1, e2, e3, row, col):
        total_energies = e1 + e2 + e3
        min_energy_index = np.argmin(total_energies)
        new_row = row + min_energy_index // 7 - 3
        new_col = col + min_energy_index % 7 - 3
        return new_row, new_col

    # Other methods such as `update_points`, `calculate_area`, `calculate_perimeter`, etc. should follow the same pattern.
    # They will be methods of this class with the necessary adjustments to work with class attributes and methods.

    # Method to process and display the final image
    def process_and_display(self):
        # Initialize contour points if not already done
        if not self.contour_points:
            # Placeholder for initializing contour points, you'll need to implement this
            self.initialize_contour_points()

        for iteration in range(100):  # Example: 100 iterations, adjust as necessary
            new_contour_points = []
            for idx, point in enumerate(self.contour_points):
                row, col = point
                next_point = self.contour_points[(idx + 1) % len(self.contour_points)]
                prior_point = self.contour_points[idx - 1]

                # Calculate energies
                elastic_energy = self.calc_elastic_energy(1, row, col, next_point)
                smooth_energy = self.calc_smooth_energy(1, row, col, next_point, prior_point)
                external_energy = self.calc_external_energy(1, row, col)

                # Sum energies and get new point location
                new_row, new_col = self.sum_energies(elastic_energy, smooth_energy, external_energy, row, col)
                new_contour_points.append((new_row, new_col))

            # Update contour points for the next iteration
            self.contour_points = new_contour_points

            # Optional: Display or save the image with the updated contour
            # You might create a separate method to handle visualization if needed
            self.display_contour()

        # After all iterations, you might want to display the final result or save it
        self.finalize_display()

