from PIL import Image
import pytesseract
import platform
import os

if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
else:
    tesseract_cmd = os.getenv("TESSERACT_CMD", "/usr/bin/tesseract")
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

img = Image.open('ocr_text_image.png')

text = pytesseract.image_to_string(img)

print(text)
