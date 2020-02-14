# Author: gabri
# File: interface_grafica
# Date: 17/11/2019
# Made with PyCharm

# Standard Library
import sys

# Third party modules
from PyQt5.QtWidgets import QMainWindow, QApplication

# Local application imports
from main_window import Ui_MainWindow
from serial_device import SerialDevice


class VoltageController(SerialDevice):
    def send_voltage(self, value):
        data = bytes(f"{value:04.1f}", "utf-8")
        data = data[0:2] + data[3:4]  # Tira o ponto fora
        if self.debug:
            print(f"Tensão: {data}")
        if self.isWritable():
            self.write(data)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.voltage = 0.0
        self.min_voltage = 0.0
        self.max_voltage = 24.0
        self.voltage_controller = VoltageController(debug=True)

        self.ui.output_voltage_slider.sliderMoved.connect(
            self.output_voltage_slider_moved)
        self.ui.output_voltage_slider.sliderReleased.connect(
            self.output_voltage_slider_released)

    def change_voltage_label(self):
        self.voltage = float(self.ui.output_voltage_slider.value())
        self.voltage = self.voltage * (
                self.max_voltage - self.min_voltage) / 200.0 + self.min_voltage
        self.ui.output_voltage_label.setText(str(self.voltage) + " V")

    def output_voltage_slider_released(self):
        self.change_voltage_label()
        self.voltage_controller.send_voltage(self.voltage)

    def output_voltage_slider_moved(self):
        self.change_voltage_label()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
