import sys
import random
import string
import cv2 as cv

#randomize the dimensions of the image
def randomize_dimensions(img):
    img = cv.resize(img, (random.randint(100, 1000), random.randint(100, 1000)))
    return img
#recolor the image
def random_filter(img):
    filters = [cv.COLOR_BGR2GRAY, cv.COLOR_BGR2HSV, cv.COLOR_BGR2HLS,
               cv.COLOR_BGR2LAB, cv.COLOR_BGR2LUV, cv.COLOR_BGR2XYZ,
               cv.COLOR_BGR2YCrCb, cv.COLOR_BGR2YUV]
    img = cv.cvtColor(img, random.choice(filters))
    return img
def main():
    while True:
        img = cv.imread("cc.jpg", cv.IMREAD_ANYCOLOR)
        img = randomize_dimensions(img)
        img = random_filter(img)
        cv.imshow(str(''.join(random.choices(
    string.ascii_letters, k=random.randint(30, 80)))), img)
        if cv.waitKey(0) == 27:
            cv.destroyAllWindows()
            sys.exit()
        cv.destroyAllWindows()
if __name__ == '__main__':
    main()
