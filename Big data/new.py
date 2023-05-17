import pytesseract as pst
import PIL.Image as pi
from pytesseract import Output
from wand.image import Image as wii
from pdf2image import convert_from_path
from collections import Counter
from glob import glob as gg

# Text recognition configuration
MY_CONFIG = r"--psm 3 --oem 3 -l kaz" # --psm 3, 6 

from natsort import natsorted

PNG_FILES = natsorted(gg('./png2/*.png'))


text_list_doc = []

for file in PNG_FILES:
    test_text = pst.image_to_string(pi.open(file), config = MY_CONFIG)
    text_list_doc += test_text.split('?')


new_list = []

for text in text_list_doc:
    text_list = text.split('\n')
    text = text_list[-1]
    new_list.append(text)

without_index = []

for text in new_list:
    text_list = text.split('. ')
    text = text_list[-1]
    without_index.append(text)


counter = Counter(without_index)
duplicates = [element for element, count in counter.items() if count > 1]

for duplicate in duplicates:
    print(duplicate)