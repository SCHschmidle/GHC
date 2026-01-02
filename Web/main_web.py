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
        print(f"Debug: image_path = {image_path}, type = {type(image_path)}")  # Logging zur Konsole
        
        if image_path is True:
            # Workaround: Annahme, dass das Bild in "clipboard_image.png" gespeichert wurde
            image_path = "clipboard_image.png"
        elif not image_path or not isinstance(image_path, str):
            return templates.TemplateResponse(
                "index.html",
                {"request": request, "name": "GHC", "ocr_result": f"Fehler: Kein gültiges Bild in der Zwischenablage gefunden. Debug: {image_path} (Typ: {type(image_path)})"}
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