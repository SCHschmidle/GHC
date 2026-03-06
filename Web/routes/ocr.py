from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
from pathlib import Path

from Web.OCR_web import save_clipboard_image, OCR_clipboard_image, delete_clipboard_image
from ghc.main import set_data, get_end_times

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).parent.parent / "templates"))

user, target_location, walking_time, minus_time, target, lunch_time = set_data()


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

        ocr_full_text, ocr_times = OCR_clipboard_image(image_path)
        delete_clipboard_image(image_path)

        times = [datetime.strptime(zeit, "%H:%M") for zeit in ocr_times]

        end_time = get_end_times(times, lunch_time, target)
        print(f"Debug: end_time = {end_time}, lunch_time = {lunch_time}, target = {target}")

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "name": "GHC",
                "ocr_result": ", ".join(ocr_times),
                "end_time": end_time,
                "full_ocr_text": ocr_full_text
            }
        )

    except Exception as e:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "name": "GHC", "ocr_result": f"Fehler: {str(e)}"}
        )
