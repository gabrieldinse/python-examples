import cv2
import matplotlib.pyplot as plt
import skimage
from skimage import img_as_float, img_as_ubyte, transform
from skimage.color import rgb2gray


def grab_frame(cap, size):
    ret, frame = cap.read()
    image = img_as_float(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    scaled_image = transform.resize(image, size)
    gray_scaled_image = rgb2gray(scaled_image)
    return gray_scaled_image


def main():
    # Initiate the two cameras
    cap = cv2.VideoCapture(0)

    while True:
        image = grab_frame(cap, (600, 600))
        cv2.imshow('frame', img_as_ubyte(image))
        plt.pause(0.01)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()


if __name__ == '__main__':
    main()
