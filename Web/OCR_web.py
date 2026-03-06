from PIL import ImageGrab
import os
import easyocr
import re

path = "clipboard_screenshot.png"
ocr_reader = None

def get_ocr_reader():
    global ocr_reader
    if ocr_reader is None:
        ocr_reader = easyocr.Reader(['de', 'en'])
    return ocr_reader

def save_clipboard_image():
    img = ImageGrab.grabclipboard()

    if img is None:
        return False

    img.save(path)
    return path  

def OCR_clipboard_image(image_path):
    reader = get_ocr_reader()
    result = reader.readtext(image_path)
    text = ' '.join([line[1] for line in result])

    processed_text = re.sub(r'[.,;]', ':', text)

    processed_text = re.sub(r'(\d)\s+(\d)', r'\1\2', processed_text)

    processed_text = re.sub(r'\s*:\s*', ':', processed_text)

    zeiten = re.findall(r'\b([012]?\d):([0-5]\d)\b', processed_text)

    formatted_zeiten = [f"{h}:{m}" for h, m in zeiten]

    return text, formatted_zeiten

def delete_clipboard_image(image_path):
    if os.path.exists(image_path):
        os.remove(image_path)