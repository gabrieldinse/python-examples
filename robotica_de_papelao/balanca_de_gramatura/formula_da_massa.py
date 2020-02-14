# Author: gabri
# File: formula_da_massa
# Date: 17/09/2019
# Made with PyCharm

# Standard Library
import numpy as np

# Third party modules

# Local application imports


def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


def main():
    degree_to_rad = np.pi/180
    m1 = 4.1 * 5
    m0 = 9.2
    ml = 10.0
    r2v = np.array([3.063, -24.187], dtype=float)
    r2 = np.linalg.norm(r2v)
    r1a = np.array([-77.194, 17.813], dtype=float)
    r1b = np.array([-37.150, 2.449], dtype=float)
    r1v = (m1*r1a + ml * r1b) / (m1 + ml)
    r1 = np.linalg.norm(r1v)
    phi = angle_between(r1v, r2v) / degree_to_rad
    r_alpha = np.array([-1, 0], dtype=float)
    psi = angle_between(r_alpha, r1v) / degree_to_rad

    print('m1: {}'.format(m1))
    print('m0: {}'.format(m0))
    print('phi: {}'.format(phi))
    print('r1: {}'.format(r1))
    print('r2: {}'.format(r2))

    # Escolher
    for alpha in np.arange(0, 90.2, 0.2):
        beta = alpha + psi
        m = m1 * (np.sin(degree_to_rad * beta) / np.cos(degree_to_rad * (-phi + 90 + beta))) * (r1 / r2) - m0
        print('alpha: {:.4} | m = {:.4}'.format(alpha, m))


if __name__ == "__main__":
    main()
