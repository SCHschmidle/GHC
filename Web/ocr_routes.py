from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from Web.OCR_web import save_clipboard_image, OCR_clipboard_image, delete_clipboard_image

from ghc.main import *

user, target_location, walking_time, minus_time, target, lunch_time = set_data()

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post("/ocr", response_class=HTMLResponse)
async def process_ocr(request: Request):
    try:
        image_path = save_clipboard_image()
        print(f"Debug: image_path = {image_path}, type = {type(image_path)}")

        if not image_path or not isinstance(image_path, str):
            return templates.TemplateResponse(
                "index.html",
                {"request": request, "name": "GHC", "ocr_result": f"Fehler: Kein gültiges Bild in der Zwischenablage gefunden. Debug: {image_path} (Typ: {type(image_path)})"}
            )

        ocr_text = OCR_clipboard_image(image_path)
        delete_clipboard_image(image_path)

        ocr_text = [datetime.strptime(zeit, "%H:%M") for zeit in ocr_text] 

        
        end_time = get_end_times(ocr_text,lunch_time,target)
        print(f"Debug: end_time = {end_time}, lunch_time = {lunch_time}, target = {target}")


        return templates.TemplateResponse(
            "index.html",
            {"request": request, "name": "GHC", "ocr_result": ocr_text, "end_time": end_time}
        )
    
    except Exception as e:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "name": "GHC", "ocr_result": f"Fehler: {str(e)}"}
        )