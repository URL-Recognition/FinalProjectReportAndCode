import URL_Detector
import ImageOCR

Detector = URL_Detector.URL_Detector()
Detector.perform_training('URL_files/URLS.txt', 'URL_files/NonURLS.txt')

OCR = ImageOCR.ImageOCR()

txt = OCR.get_word_list('images/test3.png', True)

testURLs = Detector.classify_array(txt)

print(testURLs)
print(txt)

