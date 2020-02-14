# Author: gabri
# File: pre_processamento
# Date: 16/09/2019
# Made with PyCharm

from __future__ import print_function

# Standard Library
import os
import sys

# Third party modules
import keras
from keras.datasets import mnist
from keras.models import Sequential
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


class AccuracyHistory(keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        self.losses = []
        self.acc = []

    def on_epoch_end(self, batch, logs={}):
        self.losses.append(logs.get('loss'))
        self.acc.append(logs.get('acc'))


def main():
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

    train_data = AccuracyHistory()

    model = Sequential()
    model.add(Conv2D(32, kernel_size=3, activation='relu', input_shape=(img_size, img_size, 1)))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(64, kernel_size=3, activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(128, kernel_size=3, activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(2, activation='softmax'))

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    n_epochs = 20
    n_batchs = 20
    model.fit(x_train, y_train, epochs=n_epochs,
              batch_size=int(len(x_train)/n_batchs), callbacks=[train_data])

    statistic = model.evaluate(x_test, y_test, verbose=0)
    model.save(f'modelo3_{round(statistic[1] * 100, 2)}.h5')
    print("Acerto: ", round(statistic[1] * 100, 2), "%")

    fig, axs = plt.subplots(nrows=1, ncols=2)
    ax = axs[0]
    ax.plot(range(1, n_epochs+1), train_data.losses)
    ax.set_title('Losses')
    ax.set_ylabel("Loss (/100)")
    ax.set_xlabel("Epoch")

    ax = axs[1]
    ax.plot(range(1, n_epochs+1), train_data.acc)
    ax.set_title('Accuracy')
    ax.set_ylabel("Accuracy (/100)")
    ax.set_xlabel("Epoch")

    fig.suptitle('Epochs statistics')

    plt.show()

if __name__ == "__main__":
    main()
