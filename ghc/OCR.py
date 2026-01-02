from PIL import ImageGrab
import os
from rapidocr_onnxruntime import RapidOCR
import re

path="clipboard_screenshot.png"

def save_clipboard_image():
    

    img = ImageGrab.grabclipboard()

    if img is None:
        
        return False

    img.save(path)
    return "Web/clipboard_image.png"

def OCR_clipboard_image(path):
    ocr = RapidOCR()
    result, elapse = ocr(path)
    text = ' '.join([line[1] for line in result])
    text = re.sub(r'(\d{1,2})\.(\d{2})', r'\1:\2', text)
    zeiten = re.findall(r'\d{1,2}:\d{2}', text)
    return text, zeiten

def delete_clipboard_image():
    path="clipboard_screenshot.png"

    if os.path.exists(path):
        os.remove(path)