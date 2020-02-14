import cv2
import numpy as np


def nothing(x):
    pass


# Create a black image, a window
img = cv2.imread('orange6.jpg')
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('image', 1600, 900)

# create trackbars for color change
cv2.createTrackbar('red sup', 'image', 0, 255, nothing)
cv2.createTrackbar('green sup', 'image', 0, 255, nothing)
cv2.createTrackbar('blue sup', 'image', 0, 255, nothing)

cv2.createTrackbar('red inf', 'image', 0, 255, nothing)
cv2.createTrackbar('green inf', 'image', 0, 255, nothing)
cv2.createTrackbar('blue inf', 'image', 0, 255, nothing)

cv2.imshow('image', img)

while True:
    img_segment = img

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

    r_sup = cv2.getTrackbarPos('red sup', 'image')
    g_sup = cv2.getTrackbarPos('green sup', 'image')
    b_sup = cv2.getTrackbarPos('blue sup', 'image')
    r_inf = cv2.getTrackbarPos('red inf', 'image')
    g_inf = cv2.getTrackbarPos('green inf', 'image')
    b_inf = cv2.getTrackbarPos('blue inf', 'image')

    width, height, _ = img.shape
    for i in range(width):
        for j in range(height):
            if r_inf < img[i, j][0] > r_sup and \
               g_inf > img[i, j][1] > g_sup and \
               b_inf <= img[i, j][2] <= b_sup:
                img[i, j] = [0, 0, 0]

    cv2.imshow('image', img_segment)

cv2.destroyAllWindows()
