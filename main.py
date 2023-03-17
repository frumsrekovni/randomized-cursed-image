import sys
import random
import string
import cv2 as cv


def main():
    img = cv.imread("cc.jpg", cv.IMREAD_ANYCOLOR)
    while True:
        cv.imshow(str(''.join(random.choices(
            string.ascii_letters, k=random.randint(30, 80)))), img)
        cv.waitKey(0)
        sys.exit()


if __name__ == '__main__':
    main()
