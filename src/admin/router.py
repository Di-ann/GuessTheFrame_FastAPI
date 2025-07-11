from fastapi import APIRouter, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
import shutil
import os
from src.database import async_session_maker
from src.quiz.models import MediaItem, MediaType

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post("/upload")
async def upload_frame_api(
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

    return JSONResponse(status_code=201, content={"message": "Кадр успешно добавлен"})
