import sys
from PyQt5.QtWidgets import QApplication, QTabWidget, QFileDialog
from PyQt5 import uic
from PyQt5 import QtWidgets
import cv2
import time
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont
import pyqtgraph as pg
import numpy as np
from houghTransform import houghTransformShapeDetection
from activeContour import ActiveContour
from ChainCode import ChainCode
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import  Figure

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
        self.active_contour_instance = None
        self.houghTransform = houghTransformShapeDetection(self)
        self.handle_buttons()
       
        
# -----------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------
    def handle_buttons(self):
        self.Points_Slider.valueChanged.connect(self.implement_contour)
        self.iterations_Slider.valueChanged.connect(self.implement_contour)
        self.Points_Slider.valueChanged.connect(self.sliderPoints_value)
        self.iterations_Slider.valueChanged.connect(self.sliderIterations_value)

    def sliderPoints_value(self):
        points_value = self.Points_Slider.value()
        self.points_label.setText(f"{points_value}")

    def sliderIterations_value(self):
        iterations_value = self.iterations_Slider.value()
        self.iterations_label.setText(f"{iterations_value}")

    def browse_image_HoughDetection(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Image", "",
                                                "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.webp)",
                                                options=options)
        if file_name:
            self.selected_image_path = file_name
            self.display_image_on_graphics_layout_HoughDetection(file_name)
            self.houghTransform.detectShape()


    # def browse_image_ActiveContour(self):
    #     options = QFileDialog.Options()
    #     file_name, _ = QFileDialog.getOpenFileName(self, "Select Image", "",
    #                                             "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.webp)",
    #                                             options=options)
    #     if file_name:
    #         self.selected_image_path = file_name
    #         active_contour_instance = ActiveContour(file_name)
    #         self.display_image_on_graphics_layout_ActiveContour(file_name)

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
    
    def display_image(self,graphics_widget,image_data):
        """Utility function to display an image in a given graphics layout widget."""
        if image_data is not None:
            # Clear the previous image if any
            graphics_widget.clear()
            # Convert image data to the right format (adding a channel dimension)
            # image_data_formatted = image_data[..., np.newaxis]
            image_data = np.rot90(image_data, -1)
            # Create a PlotItem or ViewBox
            view_box = graphics_widget.addViewBox()
            # Create an ImageItem and add it to the ViewBox
            image_item = pg.ImageItem(image_data)
            view_box.addItem(image_item)
            # Adjust the view to fit the image
            # view_box.autoRange()
            # view_box.disableAutoRange()
            # self.ax.clear()
            # self.ax.imshow(cv2.cvtColor(image_data, cv2.IMREAD_GRAYSCALE))
            # scene = QtWidgets.QGraphicsScene()
            # canvas = FigureCanvasQTAgg(self.fig)
            # self.graphicsView.setScene(scene)
            # scene.addWidget(canvas)
            # self.fig.canvas.draw()
            
        else:
            print("Image data is not available.")

    def browse_image_ActiveContour(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Image", "",
                                                "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.webp)",
                                                options=options)
        if file_name:
            self.active_contour_instance = ActiveContour(file_name,self)
            gray_image = self.active_contour_instance.get_gray_image_data()
            edge_image = self.active_contour_instance.get_edge_image_data()
            self.display_image(self.graphics_beforeActiveContour, gray_image)
            # active_contour_instance.handle_buttons()
           

    def implement_contour(self):
        print("llllll")
       
        all_img, self.area_list , self.perimeter_list = self.active_contour_instance.Init_contour()
        self.contour_points = self.active_contour_instance.contour_points


        # Create a QTimer instance
        self.timer = QTimer()
        self.timer.timeout.connect(self.display_next_image)
        
        # Initialize index to track the current image being displayed
        self.image_index = 0

        # Start the timer
        self.timer.start(50)  # Adjust the interval (milliseconds) as needed

        # Store all_img in self to access it in display_next_image
        self.all_img = all_img
        

    def display_next_image(self):
        if self.image_index < len(self.all_img):
            img = self.all_img[self.image_index]
        
            self.textEdit_area.clear()
            self.textEdit_perimeter.clear()
           
        
            self.textEdit_area.append(str(self.area_list[self.image_index]))
            self.textEdit_perimeter.append(str(np.round(self.perimeter_list[self.image_index],2)))
            self.display_image(self.graphics_afterActiveContour,img)
            self.image_index += 1
        else:
            # Stop the timer when all images have been displayed
            self.timer.stop()
            chain_code_instance = ChainCode()
            chain_code_instance.print_chain_code(self.contour_points)
        

        


                



            # Display the Canny edge processed image in graphics_afterActiveContour
          

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