# Author: gabri
# File: teste
# Date: 08/10/2019
# Made with PyCharm


import sys

from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, \
    QFileDialog
from PyQt5.QtGui import QIcon

from keras.models import load_model

import matplotlib.pyplot as plt

from skimage.io import imread
from skimage.transform import resize


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Treino'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.model = load_model('modelo3_87.65.h5')
        self.model.summary()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        filename = self.openFileNameDialog()
        while filename:
            filename = self.openFileNameDialog()
        sys.exit(0)

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self,
                                                  "QFileDialog.getOpenFileName()",
                                                  "",
                                                  "All Files (*);;Python Files (*.py)",
                                                  options=options)
        if filename:
            im = imread(filename, as_gray=True, plugin='matplotlib')
            im = resize(im, (224, 224), anti_aliasing=False)
            im_test = im.reshape(1, 224, 224, 1)
            img_class = self.model.predict_classes(im_test)
            prediction = img_class[0]
            classname = img_class[0]
            if classname == 0:
                print('Carro, classe 0')
            elif classname == 1:
                print('Moto, classe 1')
            plt.imshow(im, cmap='gray')
            plt.show()
        return filename


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
