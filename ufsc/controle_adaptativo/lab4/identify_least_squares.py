# Author: Gabriel Dinse
# File: identify_least_squares
# Date: 10/6/2020
# Made with PyCharm

# Standard Library

# Third party modules
import numpy as np

# Local application imports


def identify_least_squares(L, x, y, indx, indy):
    """

    Parameters
    ----------
    L : Number of samples to be used for the system estimation. Should be
    <= len(x)
    x : Input array (samples)
    y : Output array (samples
    indx : Array with True or False values, indicating transfer function's
    numerator format
    indy : Array with True or False values, indicating transfer function's
    denominator format

    Returns
    -------
    numz : Array containing numerator coeficients of the transfer function
    denz : Array containing denominator coeficients of the transfer function

    """
    num_coefs = np.count_nonzero(indx) + np.count_nonzero(indy)
    indexes_num = np.arange(0, len(indx), 1)
    indexes_den = np.arange(0, len(indy), 1)
    U = np.zeros((L, num_coefs))
    x_history = np.zeros(len(indx))
    y_history = np.zeros(len(indy))

    for n in range(L):
        x_history[1:] = x_history[:-1]
        x_history[0] = x[n]
        y_history[1:] = y_history[:-1]
        y_history[0] = y[n]
        U[n] = np.concatenate([x_history[indx], -y_history[indy]])
    Ut = U.transpose()

    # (Ut * U)^-1 * Ut * y
    theta = np.matmul(np.linalg.inv(np.matmul(Ut, U)), np.matmul(Ut, y[:L]))

    numz = np.zeros(len(indx))
    denz = np.zeros(len(indy))
    denz[0] = 1
    theta_index = 0

    for index, belong in zip(indexes_num, indx):
        if belong:
            numz[index] = theta[theta_index]
            theta_index += 1
    for index, belong in zip(indexes_den, indy):
        if belong:
            denz[index] = theta[theta_index]
            theta_index += 1

    return numz, denz