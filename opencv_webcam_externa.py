import cv2
import numpy as np

cam = cv2.VideoCapture(1)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
# Resolucao da webcam 480x640
kernel = np.ones((5, 5), np.uint8)

while True:
    ret, frame = cam.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('gray', gray)
    dilated_img = cv2.dilate(gray, np.ones((5, 5), np.uint8))
    cv2.imshow('dilated_img', dilated_img)
    bg_img = cv2.medianBlur(dilated_img, 21)
    cv2.imshow('bg_img', bg_img)
    diff_img = 255 - cv2.absdiff(gray, bg_img)
    cv2.imshow('diff_img', diff_img)
    norm_img = diff_img.copy()
    cv2.normalize(diff_img, norm_img, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
    cv2.imshow('norm_img', norm_img)
    ret, thresh = cv2.threshold(norm_img, 100, 255, cv2.THRESH_BINARY)
    img = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    cv2.imshow('img', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
