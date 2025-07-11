import random
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.quiz.models import MediaItem

BASE_URL = "http://localhost:8000"

async def get_quiz_question(session: AsyncSession) -> dict:
    count_result = await session.execute(
        select(func.count()).select_from(MediaItem)
    )
    total_items = count_result.scalar_one()

    if total_items < 5:
        print("[DEBUG] Недостаточно кадров: всего", total_items)
        raise ValueError("В базе должно быть хотя бы 5 кадров для викторины.")

    # Выбираем случайный кадр
    offset = random.randint(0, total_items - 1)
    result = await session.execute(
        select(MediaItem).offset(offset).limit(1)
    )
    selected_item = result.scalar_one()

    if not selected_item.image_url:
        raise ValueError("У выбранного кадра нет image_url")

    # Получаем другие названия
    result = await session.execute(
        select(MediaItem.title)
        .where(MediaItem.id != selected_item.id)
        .order_by(func.random())
        .limit(4)
    )
    other_titles = [row[0] for row in result.all() if row[0]]

    if len(other_titles) < 4:
        raise ValueError("Недостаточно альтернативных названий для вариантов.")

    options = other_titles + [selected_item.title]
    random.shuffle(options)

    return {
        "media_item_id": selected_item.id,
        "image_url": BASE_URL + selected_item.image_url,
        "options": options
    }
