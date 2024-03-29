import sys
from PyQt5.QtWidgets import QApplication, QTabWidget, QFileDialog
from PyQt5 import uic
import cv2
import pyqtgraph as pg
import numpy as np
from houghTransform import houghTransformShapeDetection
from activeContour import ActiveContour


# -----------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------





class MyTabWidget(QTabWidget):
    def __init__(self, ui_file):
        super().__init__()
        uic.loadUi(ui_file, self)
        self.image_edges = pg.GraphicsLayoutWidget()
        self.selected_image_path = None
        self.pushButton_browseImage_HoughDetection.clicked.connect(self.browse_image_HoughDetection)
        self.pushButton_browseImage_ActiveContour.clicked.connect(self.browse_image_ActiveContour)
        self.houghTransform = houghTransformShapeDetection(self)

# -----------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------

    def browse_image_HoughDetection(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Image", "",
                                                "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.webp)",
                                                options=options)
        if file_name:
            self.selected_image_path = file_name
            self.display_image_on_graphics_layout_HoughDetection(file_name)
            self.houghTransform.detectShape()


    def browse_image_ActiveContour(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Image", "",
                                                "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.webp)",
                                                options=options)
        if file_name:
            self.selected_image_path = file_name
            active_contour_instance = ActiveContour(file_name)
            self.display_image_on_graphics_layout_ActiveContour(file_name)

# -----------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------

    def display_image_on_graphics_layout_HoughDetection(self, image_path):
        image_data = cv2.imread(image_path)
        image_data = cv2.cvtColor(image_data, cv2.COLOR_BGR2GRAY)
        image_data = np.rot90(image_data, -1)
        # Clear the previous image if any
        self.graphics_beforeHoughDetection.clear()
        # Create a PlotItem or ViewBox
        view_box = self.graphics_beforeHoughDetection.addViewBox()
        # Create an ImageItem and add it to the ViewBox
        image_item = pg.ImageItem(image_data)
        view_box.addItem(image_item)
        # Optional: Adjust the view to fit the image
        view_box.autoRange()


    def display_image(self, graphics_widget, image_data):
        """Utility function to display an image in a given graphics layout widget."""
        if image_data is not None:
            # Clear the previous image if any
            graphics_widget.clear()
            # Convert image data to the right format (adding a channel dimension)
            image_data_formatted = image_data[..., np.newaxis]
            # Create a PlotItem or ViewBox
            view_box = graphics_widget.addViewBox()
            # Create an ImageItem and add it to the ViewBox
            image_item = pg.ImageItem(image_data_formatted)
            view_box.addItem(image_item)
            # Adjust the view to fit the image
            view_box.autoRange()
        else:
            print("Image data is not available.")

    def browse_image_ActiveContour(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Image", "",
                                                "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.webp)",
                                                options=options)
        if file_name:
            active_contour_instance = ActiveContour(file_name)
            gray_image = active_contour_instance.get_gray_image_data()
            edge_image = active_contour_instance.get_edge_image_data()

            # Display the grayscale image in graphics_beforeActiveContour
            self.display_image(self.graphics_beforeActiveContour, gray_image)

            # Display the Canny edge processed image in graphics_afterActiveContour
            self.display_image(self.graphics_afterActiveContour, edge_image)


# -----------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------

    def keyPressEvent(self, event):
        if event.key() == 16777216:         # Integer value for Qt.Key_Escape
            if self.isFullScreen():
                self.showNormal()           # Show in normal mode
            else:
                self.showFullScreen()       # Show in full screen
        else:
            super().keyPressEvent(event)
    
# -----------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------


def main():
    app = QApplication(sys.argv)
    window = MyTabWidget("MainWindow.ui")
    window.showFullScreen()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()