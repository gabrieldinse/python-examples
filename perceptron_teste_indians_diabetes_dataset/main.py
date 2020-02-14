# Author: gabri
# File: perceptron_teste_indians_diabetes_dataset
# Date: 25/08/2019
# Made with PyCharm

# Standard Library
import numpy as np
from perceptron import Perceptron, step
import csv

# Third party modules

# Local application imports


def main():
    p = Perceptron(8, 0.05)
    dataset = np.loadtxt('pima-indians-diabetes.data.csv', delimiter=',')
    desired_outputs = dataset[:, -1:]
    inputs = dataset[:, :-1]
    print(desired_outputs)
    print(inputs)

    # p = Perceptron(2, 0.1)
    # desired_outputs = [-1, 1, 1, -1]
    # inputs = [[1, 1], [1, -1], [-1, 1], [-1, -1]]

    num_epochs = 500
    p.train(inputs, desired_outputs, num_epochs, batch_size=1, debug=False)


if __name__ == "__main__":
    main()
