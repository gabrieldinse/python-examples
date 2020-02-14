# Author: gabri
# File: avaliar_modelo
# Date: 29/10/2019
# Made with PyCharm

# Standard Library
import os

# Third party modules
import keras
from keras.datasets import mnist
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
from skimage.transform import resize
import numpy as np
from skimage.io import imread
from skimage.transform import resize
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# Local application imports


def main():
    model = load_model('modelo3_87.65.h5')
    model.summary()

    folder = os.path.dirname(os.path.abspath(__file__))
    folder = os.path.join(folder, 'dataset')
    x = []
    # (carro,motocicleta)
    y = []
    img_size = 224
    for filename in os.listdir(folder):
        if '.jpg' in filename:
            filepath = os.path.join(folder, filename)
            im = imread(filepath, as_gray=True, plugin='matplotlib')
            im = resize(im, (img_size, img_size), anti_aliasing=False)
            x.append(im)
            if 'carro' in filename:
                y.append((1, 0))
            elif 'moto' in filename:
                y.append((0, 1))
            else:
                raise RuntimeError("Erro em label da imagem.")
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)
    x_train, x_test, y_train, y_test = (np.array(x_train), np.array(x_test),
                                        np.array(y_train), np.array(y_test))
    x_train = x_train.reshape(x_train.shape[0], img_size, img_size, 1)
    x_test = x_test.reshape(x_test.shape[0], img_size, img_size, 1)
    statistic = model.evaluate(x_test, y_test, verbose=1)
    print(statistic)

if __name__ == "__main__":
    main()
