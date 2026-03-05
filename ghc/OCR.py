from PIL import ImageGrab
import os
import pytesseract
import re

path="clipboard_screenshot.png"

def save_clipboard_image():
    

    img = ImageGrab.grabclipboard()

    if img is None:
        
        return False

    img.save(path)
    return True

def OCR_clipboard_image(path):
    text = pytesseract.image_to_string(path)
    text = re.sub(r'(\d{1,2})\.(\d{2})', r'\1:\2', text)
    zeiten = re.findall(r'\d{1,2}:\d{2}', text)
    return text, zeiten

def delete_clipboard_image():
    path="clipboard_screenshot.png"

    if os.path.exists(path):
        os.remove(path)