import sys
import random
import string
import cv2 as cv

#randomize the dimensions of the image
def randomize_dimensions(img):
    img = cv.resize(img, (random.randint(40, 3000), random.randint(40, 3000)))
    return img
#recolor the image
def random_filter(img):
    filters = [cv.COLOR_BGR2GRAY, cv.COLOR_BGR2HSV, cv.COLOR_BGR2HLS,
               cv.COLOR_BGR2LAB, cv.COLOR_BGR2LUV, cv.COLOR_BGR2XYZ,
               cv.COLOR_BGR2YCrCb, cv.COLOR_BGR2YUV]
    img = cv.cvtColor(img, random.choice(filters))
    return img


#if I press the S key it saves the image to the folder as a png
def save_image(img,filename):
    filename = "chicks/" + filename + ".png"
    cv.imwrite(filename, img)
    print("Image",filename,"saved!")





def main():
    while True:
        img = cv.imread("cc.jpg", cv.IMREAD_ANYCOLOR)
        img = randomize_dimensions(img)
        img = random_filter(img)
        filename = str(''.join(random.choices(
    string.ascii_letters, k=random.randint(30, 80))))
        cv.imshow(filename, img)
        k = cv.waitKey(0)
        if k == 27:
            cv.destroyAllWindows()
            sys.exit()
        elif k == ord('s'):
            save_image(img,filename)
        cv.destroyAllWindows()
if __name__ == '__main__':
    main()
