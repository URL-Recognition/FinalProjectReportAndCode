import cv2
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'

class ImageOCR:

    #CHARACTER_WHITELIST = "-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~:/?#[]@!$&'()*+,;=`._ -psm 6"

    def pre_process(self,image_file,save = False):
        """
        :param image_file: The image file name to preprocess
        :param save: Set to true if you want preprocessed image to be saved (Optional)
        """

        # read in image
        image = cv2.imread(image_file)
        # make image grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # resize image to be of 2x original size
        rsize = cv2.resize(gray, None, 2, 2, cv2.INTER_CUBIC)
        # apply adaptive threshold and conversion to binary image, this works best with blur
        prep2 = cv2.adaptiveThreshold(rsize, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 12)
        # apply median blur to clean pepper noise
        prep2 = cv2.medianBlur(prep2, 3)

        if(save):
            #create image name
            ind = image_file.rfind('.')#Get index of last period
            save_name = image_file[:ind] + '_processed' + image_file[ind:]
            # save image to new name
            cv2.imwrite(save_name, prep2)
            return [prep2, save_name]

        return prep2

    def do_OCR(self,image_file,preprocess = True):

        #Perform preprocessing operation
        if(preprocess):
            image = self.pre_process(image_file, False)
        else:
            image = cv2.imread(image_file)

        return pytesseract.image_to_string(Image.fromarray(image))

    def get_word_list(self,image_file,preprocess=True):
        txt = self.do_OCR(image_file,preprocess)
        return txt.split()

# #The rest of the code here should occur after preprocessing
#
#
# def cleanstring(s):
#     dict = [('|', 'l'), ('—', '-')]
#     for i in dict:
#         if i[0] in s:
#             s = s.replace(i[0], i[1])
#     return s
#
# #replace '|' and '—' with 'l' and '-'
# text = cleanstring(text)
#
# #print entirety of read
# print(text)


