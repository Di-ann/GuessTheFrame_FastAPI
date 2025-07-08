from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Form
from src.quiz.models import MediaItem

from src.database import get_async_session
from src.quiz.service import get_quiz_question


router = APIRouter(prefix="/quiz", tags=["Quiz"])

templates = Jinja2Templates(directory="src/templates")

@router.get("/page", response_class=HTMLResponse)
async def quiz_page(request: Request, session: AsyncSession = Depends(get_async_session)):
    question = await get_quiz_question(session)
#     question = {
#     "media_item_id": 1,
#     "image_url": "/static/images/example.jpg",
#     "options": ["Example A", "Example B", "Example C", "Example D", "Example E"]
# }
    return templates.TemplateResponse(
        "quiz_question.html",
        {
            "request": request,
            "media_item_id": question["media_item_id"],
            "image_url": question["image_url"],
            "options": question["options"]
        }
    )

@router.post("/answer", response_class=HTMLResponse)
async def check_answer(
    request: Request,
    media_item_id: int = Form(...),
    selected_title: str = Form(...),
    session: AsyncSession = Depends(get_async_session)
):
    # Получаем правильный ответ
    db_item = await session.get(MediaItem, media_item_id)
    is_correct = db_item.title.strip().lower() == selected_title.strip().lower()

    # (опционально) сохранить результат в UserAnswer

    return templates.TemplateResponse(
        "quiz_feedback.html",
        {
            "request": request,
            "is_correct": is_correct,
            "correct_title": db_item.title
        }
    )
