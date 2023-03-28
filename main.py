import sys
import tkinter as tk
from tkinter.filedialog import askopenfilename
import random
import string
import cv2 as cv

allowed_filename_characters = string.hexdigits + "!#$%&'()+,-;=@[]^_`{}~"

#randomize the dimensions of the image
def randomize_dimensions(img):
    img = cv.resize(img, (random.randint(20, 2000), random.randint(20, 2000)))
    return img
#recolor the image
def random_recolor(img):
    filters = [cv.COLOR_BGR2GRAY, cv.COLOR_BGR2HSV, cv.COLOR_BGR2HLS,
               cv.COLOR_BGR2LAB, cv.COLOR_BGR2LUV, cv.COLOR_BGR2XYZ,
               cv.COLOR_BGR2YCrCb, cv.COLOR_BGR2YUV]
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
    cv.imwrite(filename + ".png", img)
    print("Image",filename,"saved!´")
    popupmsg(msg="Image "+filename+" saved!")

#when the user presses the X button the image will close
def on_closing():
    cv.destroyAllWindows()
    sys.exit()

def main():
    original_image = askopenfilename()
    print(original_image) 
    while True:
        img = cv.imread(original_image, cv.IMREAD_ANYCOLOR)
        img = randomize_dimensions(img)
        img = random_recolor(img)
        filename = str(''.join(random.choices(allowed_filename_characters, k=random.randint(24, 48))))
        cv.imshow(filename, img)
        k = cv.waitKey(0)
        if k == 27:
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
        cv.destroyAllWindows()
if __name__ == '__main__':
    main()
