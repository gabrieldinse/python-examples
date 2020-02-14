import cv2

img = cv2.imread("C:/Users/dell/Desktop/objects.JPG")
print('shape for RGB image: {}'.format(img.shape))
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print('shape for gray image: {}'.format(img.shape))

# Imagens binarias tem valor 0 ou 255 (e nao 0 ou 1)
_, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
print('shape for binary image: {}'.format(img.shape))
cv2.imshow('tela', img)
cv2.waitKey(0)
cv2.destroyAllWindows()