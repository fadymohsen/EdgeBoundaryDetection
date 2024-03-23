import numpy as np
import cv2
import pyqtgraph as pg

class houghTransformShapeDetection:
    def __init__(self, main_tab_widget):
        self.main_tab_widget = main_tab_widget
        self.ui = self.main_tab_widget
        self.ui.comboBox_houghDetectionMethod.activated.connect(self.detectShape)

    def detectShape(self):
        selectedShape = self.ui.comboBox_houghDetectionMethod.currentText()
        if selectedShape == "Lines":
            self.detectLines()
        elif selectedShape == "Ellipse":
            self.detectEllipse()
        else:
            self.detectCircles()

    def detectCircles(self):
        pass
    
    def detectLines(self):
        pass

    def detectEllipse(self):
        pass