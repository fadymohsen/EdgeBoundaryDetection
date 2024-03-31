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



# -----------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------

    def display_image_on_graphics_layout_HoughDetection(self, image_path):
        image_data = cv2.imread(image_path)
        image_data = cv2.cvtColor(image_data, cv2.COLOR_BGR2GRAY)
        image_data = np.rot90(image_data, -1)
        self.graphics_beforeHoughDetection.clear()
        view_box = self.graphics_beforeHoughDetection.addViewBox()
        image_item = pg.ImageItem(image_data)
        view_box.addItem(image_item)
        view_box.autoRange()
    

    
    def display_image(self,graphics_widget,image_data):
        """Utility function to display an image in a given graphics layout widget."""
        if image_data is not None:
            graphics_widget.clear()
            image_data = np.rot90(image_data, -1)
            view_box = graphics_widget.addViewBox()
            image_item = pg.ImageItem(image_data)
            view_box.addItem(image_item)
        else:
            print("Image data is not available.")



    def browse_image_ActiveContour(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Image", "",
                                                "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.webp)",
                                                options=options)
        if file_name:
            active_contour_instance = ActiveContour(file_name,self)
            # active_contour_instance.handle_buttons()
            gray_image = active_contour_instance.get_gray_image_data()
            edge_image = active_contour_instance.get_edge_image_data()
            self.display_image(self.graphics_beforeActiveContour, gray_image)
            all_img, self.area_list , self.perimeter_list = active_contour_instance.Init_contour()
            self.contour_points = active_contour_instance.contour_points


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