import sys
import tkinter as tk
from tkinter.filedialog import askopenfilename
import random
import string
import cv2 as cv

viewport_width = 545
viewport_height = 436
allowed_filename_characters = string.hexdigits + "!#$%&'()+,-;=@[]^_`{}~"
religious_words = ["god", "jesus", "bible", "prayer", "church", "baptism", "salvation", "savior", "lord","holy", "spirit","faith", "heaven", "hell", "sin", "sinner", "repent", "repentance", "forgive", "forgiveness", "sacrifice"]

#make a list of words that sounds like it is from dante's inferno
dante_words = ["abandon", "abandonment", "abase", "abasement", "abash", "abate", "abdicate", "aberration", "abhor", "abhorrence", "abhorrent", "abide", "abject", "abjection", "abjure", "abnegation", "abolish", "abominable", "abominate", "abomination", "abort", "abound", "abrade", "abrasion", "abrogate", "abscond", "absence", "absent", "absentee", "absenteeism", "absent-minded", "absent-mindedness", "absolve", "absorb", "absorption", "abstain", "abstention", "abstinence", "abstract", "abstruse", "absurd", "absurdity", "abuse", "abusive", "abysmal", "abyss", "accede", "accelerate", "accentuate", "accept", "acceptance", "access", "accessible", "accessory", "accident", "accidental", "accidentally", "acclaim", "acclamation", "accolade", "accommodate", "accommodation", "accompaniment", "accompany", "accomplice", "accomplish", "accomplishment", "accord", "accordance", "accordingly", "account", "accountable", "accountant", "accounting", "accredit", "accreditation", "accretion", "accrue", "accumulate", "accumulation", "accuracy", "accurate", "accusation", "accuse", "accused", "accustom", "accustomed", "acerbic", "ache", "achieve", "achievement", "acid", "acidic", "acknowledge", "acknowledgment", "acquaint", "acquaintance", "acquiesce", "acquire", "acquisition", "acquit", "acquittal", "acquitted", "acre", "acrid", "acrimonious", "acrimony", "acrobatic", "acrobatics", "acronym", "across", "act", "action", "activate", "active", "activist", "activity", "actor"]


#randomly morph the image
def random_morph(img):
    img = cv.erode(img, cv.getStructuringElement(cv.MORPH_ELLIPSE, (random.randint(1, 10), random.randint(1, 10))))
    img = cv.dilate(img, cv.getStructuringElement(cv.MORPH_ELLIPSE, (random.randint(1, 10), random.randint(1, 10))))
    return img

#randomize the dimensions of the image
def randomize_dimensions(img):
    img = cv.resize(img, (random.randint(72, 720), random.randint(72, 720)))
    return img
#recolor the image
def random_recolor(img):
    filters = [cv.COLOR_BGR2GRAY, cv.COLOR_BGR2HSV, cv.COLOR_BGR2HLS,
               cv.COLOR_BGR2LAB, cv.COLOR_BGR2LUV, cv.COLOR_BGR2XYZ,
               cv.COLOR_BGR2YCrCb, cv.COLOR_BGR2YUV]
    img = cv.cvtColor(img, random.choice(filters))
    return img

#ranomdly rotate the image
def random_rotate(img):
    img = cv.rotate(img, random.randint(-180, 180))
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

#when the user presses the X button the image will close
def on_closing():
    cv.destroyAllWindows()
    sys.exit()


#randomly warp the image
def random_distort(img):
    img = cv.warpAffine(img, cv.getRotationMatrix2D((random.randint(100, 1000), random.randint(100, 1000)), random.randint(-20, 20), 1),(viewport_width,viewport_height))
    return img


def random_text(img, text):
    #There are 8 different fonts in OpenCV
    font = random.randint(0, 7)
    #the thickness int = pixels
    thickness = random.randint(1, 4)
    origin_coordinates = (random.randint(0, viewport_width), random.randint(0, viewport_height))
    fontScale = random.randint(1, 10)
    fontColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    lineType = random.randint(1, 10)
    cv.putText(img, text, origin_coordinates, font, fontScale, fontColor, thickness, lineType, False)
    return img

def main():
    original_image = askopenfilename()
    print(original_image) 
    while True:
        img = cv.imread(original_image, cv.IMREAD_ANYCOLOR)
        img = randomize_dimensions(img)
        img = random_recolor(img)
        img = random_morph(img)
        img = random_distort(img)
        img = random_text(img,random.choice(religious_words))
        img = random_text(img,random.choice(dante_words))
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
