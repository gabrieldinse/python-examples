# Author: gabri
# File: perceptron
# Date: 25/08/2019
# Made with PyCharm

# Standard Library
import numpy as np
import random

# Third party modules

# Local application imports


def step(x):
    if x > 0:
        return 1
    else:
        return -1


class Perceptron:
    def __init__(self, n_inputs, learning_rate, activation=np.tanh):
        self.weights = np.zeros(n_inputs + 1, dtype=float)
        self.learning_rate = learning_rate
        self.activation = activation
        self.desired_output = None

    def feedforward(self, inputs):
        self.inputs = np.array(inputs, dtype=float)
        self.summer = sum(
            self.weights * np.concatenate((self.inputs, [1])))
        self._output = self.activation(self.summer)
        self._error = float(self.desired_output) - self.output

    def adjust_weights(self):
        average_error = sum(self.batch_errors) / len(self.batch_errors)
        self.weights = \
            self.weights + \
            self.learning_rate * average_error * np.concatenate(
                (self.inputs, [1]))

    @property
    def output(self):
        return self._output

    @output.setter
    def output(self, value):
        raise AttributeError("Can't set this attribute.")

    @property
    def error(self):
        return self._error

    @error.setter
    def error(self, value):
        raise AttributeError("Can't set this attribute.")

    def __str__(self):
        return "Perceptron(weitghs={}, inputs={}, desired_ouput={}, output={}" \
               ", summer={}, error={})".format(self.weights, self.inputs,
                                               self.desired_output, self.output,
                                               self.summer, self.error)

    def train(self, inputs, desired_outputs, num_epochs, batch_size=1,
              debug=True):
        for i in range(num_epochs):
            # Randomize the order of the data
            combined = list(zip(inputs, desired_outputs))
            random.shuffle(combined)
            inputs[:], desired_outputs[:] = zip(*combined)

            # Run the epoch
            print('\n- - - - - - - -\nEpoch #{}'.format(i + 1))
            total_error = 0
            on_batch = 0
            self.batch_errors = []

            # For each input
            for j in range(len(inputs)):
                self.desired_output = desired_outputs[j]
                self.feedforward(inputs[j])
                self.batch_errors.append(self.error)
                on_batch += 1
                if on_batch == batch_size:
                    self.adjust_weights()
                    self.batch_errors = []
                    on_batch = 0
                total_error += np.abs(self.error)
                if debug is True:
                    print('{}'.format(self))
            print('Total error: {}'.format(total_error))


def main():
    pass


if __name__ == "__main__":
    main()
