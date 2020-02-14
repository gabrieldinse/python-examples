import cv2
import matplotlib.pyplot as plt
from math import sqrt


def rgb_to_xyz(rgb_image):
    xyz_image = rgb_image.copy()
    rows, cols, _ = rgb_image.shape

    for i in range(rows):
        for j in range(cols):
            rgb_color = rgb_image[i, j]
            r = (rgb_color[0] / 255)
            g = (rgb_color[1] / 255)
            b = (rgb_color[2] / 255)

            if r > 0.04045:
                r = ((r + 0.055) / 1.055) ** 2.4
            else:
                r = r / 12.92

            if g > 0.04045:
                g = ((g + 0.055) / 1.055) ** 2.4
            else:
                g = g / 12.92

            if b > 0.04045:
                b = ((b + 0.055) / 1.055) ** 2.4
            else:
                b = b / 12.92

            r = r * 100
            g = g * 100
            b = b * 100

            x = (r * 0.4124) + (g * 0.3576) + (b * 0.1805)
            y = (r * 0.2126) + (g * 0.7152) + (b * 0.0722)
            z = (r * 0.0193) + (g * 0.1192) + (b * 0.9505)
            xyz_image[i, j] = [x, y, z]

    return xyz_image


def xyz_to_hunterlab(xyz_image):
    ''' Hunter Lab values using the equations corresponding to the
    illuminant D65 (led lamp) and observer 10. '''
    hunterlab_image = xyz_image.copy()
    rows, cols, _ = xyz_image.shape
    ka = 172.10
    kb = 66.70
    xr = 94.83
    yr = 100.0
    zr = 107.38

    for i in range(rows):
        for j in range(cols):
            xyz_color = xyz_image[i, j]
            l = 100.0 * sqrt(xyz_color[1] / yr)
            a = ka * (((xyz_color[0] / xr) - (xyz_color[1] / yr)) / sqrt(xyz_color[1] / yr))
            b = kb * (((xyz_color[1] / yr) - (xyz_color[2] / zr)) / sqrt(xyz_color[1] / yr))
            hunterlab_image[i, j] = [l, a, b]

    return hunterlab_image


def rgb_to_hunterlab(rgb_image):
    return xyz_to_hunterlab(rgb_to_xyz(rgb_image))

# Usar: L = L * 100 / 255
#       a = a - 128
#       b = b - 128


def cci(hunterlab):
    return 1000 * (hunterlab[1]) / (hunterlab[0] * hunterlab[2])


img = cv2.imread('orange1.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
out = rgb_to_hunterlab(img)



plt.imshow(img)
plt.show()
