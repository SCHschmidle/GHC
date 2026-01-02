from PIL import ImageGrab
import os
from rapidocr_onnxruntime import RapidOCR
import re

path = "clipboard_screenshot.png"

def save_clipboard_image():
    img = ImageGrab.grabclipboard()

    if img is None:
        return False

    img.save(path)
    return path  # Gib den lokalen Pfad zurück (relativ zu Web/)

def OCR_clipboard_image(image_path):
    ocr = RapidOCR()
    result, elapse = ocr(image_path)
    text = ' '.join([line[1] for line in result])
    text = re.sub(r'(\d{1,2})\.(\d{2})', r'\1:\2', text)
    zeiten = re.findall(r'\d{1,2}:\d{2}', text)
    return text, zeiten

def delete_clipboard_image(image_path):
    if os.path.exists(image_path):
        os.remove(image_path)