import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QLabel
from PyQt5.QtCore import Qt

class YourApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Your App Title')
        self.setGeometry(100, 100, 400, 100)

        self.Points_Slider = QSlider(Qt.Horizontal)
        self.Points_Slider.setMinimum(0)
        self.Points_Slider.setMaximum(200)
        self.Points_Slider.setValue(100)
        self.Points_Slider.setTickInterval(10)
        self.Points_Slider.setTickPosition(QSlider.TicksBelow)
        self.Points_Slider.valueChanged.connect(self.sliderPoints_value)

        self.Iterations_Slider = QSlider(Qt.Horizontal)
        self.Iterations_Slider.setMinimum(0)
        self.Iterations_Slider.setMaximum(500)
        self.Iterations_Slider.setValue(50)
        self.Iterations_Slider.setTickInterval(10)
        self.Iterations_Slider.setTickPosition(QSlider.TicksBelow)
        self.Iterations_Slider.valueChanged.connect(self.sliderIterations_value)

        self.Points_Label = QLabel('Points: 100')
        self.Iterations_Label = QLabel('Iterations: 50')

        layout = QVBoxLayout()
        layout.addWidget(self.Points_Slider)
        layout.addWidget(self.Points_Label)
        layout.addWidget(self.Iterations_Slider)
        layout.addWidget(self.Iterations_Label)
        self.setLayout(layout)

    def sliderPoints_value(self):
        points_value = self.Points_Slider.value()
        self.Points_Label.setText(f'Points: {points_value}')

    def sliderIterations_value(self):
        iterations_value = self.Iterations_Slider.value()
        self.Iterations_Label.setText(f'Iterations: {iterations_value}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = YourApp()
    window.show()
    sys.exit(app.exec_())
