import sys
import tkinter as tk
from tkinter.filedialog import askopenfilename
import random
import string
import cv2 as cv

allowed_filename_characters = string.hexdigits + "!#$%&'()+,-;=@[]^_`{}~"

#fill a list with the words from the csv file
def fill_list(filename):
    with open(filename, "r") as file:
        file = file.read()
        file = file.split("\n")
        return file

#randomly morph the image
def random_morph(img, c):
    img = cv.erode(img, cv.getStructuringElement(cv.MORPH_ELLIPSE, (random.randint(1, 10*c), random.randint(1, 10*c))))
    img = cv.dilate(img, cv.getStructuringElement(cv.MORPH_ELLIPSE, (random.randint(1, 10*c), random.randint(1, 10*c))))
    return img

#randomize the dimensions of the image
def randomize_dimensions(img):
    img = cv.resize(img, (random.randint(72, 720), random.randint(72, 720)))
    return img
#recolor the image
def random_recolor(img):
    filters = [cv.COLOR_BGR2GRAY, cv.COLOR_BGR2HSV, cv.COLOR_BGR2HLS,
               cv.COLOR_BGR2LAB, cv.COLOR_BGR2LUV, cv.COLOR_BGR2XYZ,
               cv.COLOR_BGR2YCrCb, cv.COLOR_BGR2YUV,cv.COLOR_XYZ2RGB,
               cv.COLOR_Luv2BGR,cv.COLOR_Luv2LBGR,cv.COLOR_HLS2BGR,cv.COLOR_XYZ2BGR,
    cv.COLOR_Lab2LRGB, cv.COLOR_Lab2LBGR,cv.COLOR_LRGB2Luv]
    # all of the Color Space Conversions in OpenCV in a list as cv.
    
    img = cv.cvtColor(img, random.choice(filters))
    return img

#popup text that says the image has been saved
def popupmsg(msg):
    popup = tk.Tk()
    popup.overrideredirect(True)
    popup.geometry("+%d+%d" % (popup.winfo_screenwidth()/2, popup.winfo_screenheight()/2))
    label = tk.Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10)
    popup.after(720, popup.destroy)
    popup.mainloop()

def save_image(img,filename):
    cv.imwrite("chicks/"+filename + ".png", img)
    print("Image",filename,"saved!´")
    popupmsg(msg="Image "+filename+" saved!")

def capitalize_first_letter_on_a_coinflip(word):
    if random.randint(0, 1) == 1:
        return word[0].upper() + word[1:]
    return word[0].lower() + word[1:]

#randomly warp the image
def random_distort(img, width, height):
    img = cv.warpAffine(img, cv.getRotationMatrix2D((random.randint(100, 1000), random.randint(100, 1000)), random.randint(-20, 20), 1),(width,height))
    return img

def random_text(img, text, width, height):
    #There are 8 different fonts in OpenCV
    font = random.randint(0, 7)
    #the thickness int = pixels
    thickness = random.randint(1, 4)
    origin_coordinates = (random.randint(0, width), random.randint(0, height))
    fontScale = random.randint(1, 10)
    fontColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    lineType = random.randint(1, 10)
    cv.putText(img, text, origin_coordinates, font, fontScale, fontColor, thickness, lineType, False)
    return img


def main():
    wordlist = fill_list("words.csv")
    wordlist = list(filter(None, wordlist)) #fixes if theres an empty line in the csv file
    original_image = askopenfilename()
    images = []
    images_index = 0
    images_traversing = False
    #The cursification factor should affect the interval of intergers that are generated for the random functions and the amount of times the images are run through the random functions
    CURSIFICATION_FACTOR = 1
    while True:
        if images_traversing == False:
            img = cv.imread(original_image, cv.IMREAD_ANYCOLOR)
            img = random_recolor(img)
            # loop the amount of times the cursification factor is
            for i in range(CURSIFICATION_FACTOR):
                img = randomize_dimensions(img)
                img = random_morph(img, CURSIFICATION_FACTOR)
                img = random_distort(img,random.randint(100, 1000),random.randint(100, 1000))
            
            # add a random amount of words to the image
            for i in range(random.randint(1, 3)):
                img = random_text(img,capitalize_first_letter_on_a_coinflip(random.choice(wordlist)),random.randint(100, 1000),random.randint(100, 1000))
            filename = str(''.join(random.choices(allowed_filename_characters, k=random.randint(24, 48))))

            images.append((img, filename))
        while len(images) > 100:
            images.pop(0)
        if images_traversing != True:
            images_index = len(images) - 1
        cv.imshow(images[images_index][1], images[images_index][0])
        k = cv.waitKeyEx(0)
        if k == 27: #this is the escape key
            cv.destroyAllWindows()
            sys.exit()
        elif k == ord('s'):
            save_image(img,filename)
            continue_looping = True
            while continue_looping:
                k_continue = cv.waitKey(0)
                if k_continue != ord('s'):
                    continue_looping = False
                else:
                    continue_looping = True
        elif k == 2490368: #this is up arrow key
            CURSIFICATION_FACTOR += 1
        elif k == 2621440: # this is down arrow key
            CURSIFICATION_FACTOR -= 1
        elif k == 2424832: #this is left arrow key
            images_traversing = True
            images_index -= 1
        elif k == 2555904: #this is right arrow key
            images_traversing = False
            images_index += 1
            if images_index < (len(images) - 1):
                images_traversing = True
        if images_index < 0:
            images_index = 0
        cv.destroyAllWindows()
if __name__ == '__main__':
    main()
