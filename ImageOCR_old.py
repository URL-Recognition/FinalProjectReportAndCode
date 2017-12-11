import cv2
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
import os

class ImageOCR:

    def pre_process(self,image):
        # make image grayscale
        gray = cv2.resize(image, None, 2, 2, cv2.INTER_CUBIC)


#read in image
image = cv2.imread('images/test2.png')

#make image grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#resize image to be of 2x original size
x, y = image.shape[:2]


#apply adaptive threshold and conversion to binary image
prep2 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 12)#this works best with blur

#save result above to file
cv2.imwrite("adapthresh.jpg", prep2)


#apply median blur to clean pepper noise
prep2 = cv2.medianBlur(prep2, 3)

#save file by process-id.jpg
filename = "{}.jpg".format(os.getpid())
cv2.imwrite(filename, prep2)

#The rest of the code here should occur after preprocessing
text = pytesseract.image_to_string(Image.open(filename))

def cleanstring(s):
    dict = [('|', 'l'), ('—', '-')]
    for i in dict:
        if i[0] in s:
            s = s.replace(i[0], i[1])
    return s

#replace '|' and '—' with 'l' and '-'
text = cleanstring(text)

#print entirety of read
print(text)


