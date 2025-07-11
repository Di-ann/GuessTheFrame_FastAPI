from fastapi import APIRouter, Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Form
from src.quiz.models import MediaItem
from pydantic import BaseModel
from src.database import get_async_session
from src.quiz.service import get_quiz_question


router = APIRouter(prefix="/quiz", tags=["Quiz"])

class AnswerRequest(BaseModel):
    media_item_id: int
    selected_title: str

@router.get("/questions")
async def get_question_api(session: AsyncSession = Depends(get_async_session)):
    question = await get_quiz_question(session)
    return question

@router.post("/answer")
async def check_answer_api(data: AnswerRequest, session: AsyncSession = Depends(get_async_session)):
    # Получаем правильный ответ
    db_item = await session.get(MediaItem, data.media_item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Кадр не найден")
    is_correct = db_item.title.strip().lower() == data.selected_title.strip().lower()
    return {
        "is_correct": is_correct,
        "correct_title": db_item.title
    }

