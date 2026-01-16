import sys
from pathlib import Path
from fastapi import FastAPI

sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi.templating import Jinja2Templates
from pathlib import Path

# routers
from Web.routes.home import router as home_router
from Web.routes.ocr import router as ocr_router

app = FastAPI()

app.include_router(home_router)
app.include_router(ocr_router)

templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))


@app.get("/health")
async def health():
    return {"status": "ok"}