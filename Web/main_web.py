import sys
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ghc.OCR import save_clipboard_image, OCR_clipboard_image, delete_clipboard_image

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "name": "GHC"}
    )

@app.post("/ocr", response_class=HTMLResponse)
async def process_ocr(request: Request):
    try:
        image_path = save_clipboard_image()

        if not image_path or image_path is False:
            return templates.TemplateResponse(
                "index.html",
                {"request": request, "name": "GHC", "ocr_result": "Fehler: Kein Bild in der Zwischenablage gefunden"}
            )
        
        
        ocr_text = OCR_clipboard_image(image_path)
        
        delete_clipboard_image(image_path)
        
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "name": "GHC", "ocr_result": ocr_text}
        )
    except Exception as e:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "name": "GHC", "ocr_result": f"Fehler: {str(e)}"}
        )