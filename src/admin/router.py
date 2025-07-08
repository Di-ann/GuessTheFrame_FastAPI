from fastapi import APIRouter, Request, UploadFile, Form
from fastapi.responses import RedirectResponse
import shutil
import os
from fastapi.templating import Jinja2Templates
from src.database import async_session_maker
from src.quiz.models import MediaItem, MediaType

router = APIRouter()
templates = Jinja2Templates(directory="src/templates")
UPLOAD_DIR = "/static/images"

@router.get("/admin/upload")
async def get_upload_form(request: Request):
    return templates.TemplateResponse("upload_frame.html", {"request": request})



@router.post("/admin/upload")
async def upload_frame(
    title: str = Form(...),
    type: str = Form(...),
    genre: str = Form(None),
    difficulty: int = Form(...),
    file: UploadFile = Form(...)
):
    UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "static", "images"))
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    filename = file.filename
    save_path = os.path.join(UPLOAD_DIR, filename)
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    async with async_session_maker() as session:
        item = MediaItem(
            title=title,
            type=MediaType(type),
            genre=genre,
            difficulty=difficulty,
            image_url=f"/static/images/{filename}",
        )
        session.add(item)
        await session.commit()

    return RedirectResponse("/admin/upload", status_code=303)
