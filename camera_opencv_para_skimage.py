import cv2
import matplotlib.pyplot as plt
import skimage
from skimage import img_as_float, img_as_ubyte, transform
from skimage.color import rgb2gray


def close(event):
    if event.key == 'q':
        plt.close(event.canvas.figure)


def grab_frame(cap):
    ret, frame = cap.read()
    image = img_as_float(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    scaled_image = transform.resize(image, (28, 28))
    gray_scaled_image = rgb2gray(scaled_image)
    return gray_scaled_image


def main():
    # Initiate the two cameras
    cap = cv2.VideoCapture(0)
    im = plt.imshow(img_as_float(grab_frame(cap)), cmap='gray')
    cid = plt.gcf().canvas.mpl_connect("key_press_event", close)

    while True:
        image = grab_frame(cap)
        cv2.imshow('frame', cv2.resize(img_as_ubyte(image), (600, 600), ))
        plt.pause(0.01)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    plt.show()
    cap.release()


if __name__ == '__main__':
    main()
