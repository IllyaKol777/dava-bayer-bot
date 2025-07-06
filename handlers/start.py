from aiogram import Router, F
from aiogram.types import Message
from keyboards.reply import main_menu
from utils.texts import WELCOME_TEXT
from datetime import datetime
from sqlalchemy import select
from models import User
from database import async_session

router = Router()

@router.message(F.text.in_({"/start", "🔙 Назад"}))
async def start_handler(message: Message):
    user_id = message.from_user.id
    async with async_session() as session:
        result = await session.execute(select(User).where(User.user_id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            new_user = User(
                user_id=user_id,
                full_name=message.from_user.full_name,
                username=message.from_user.username,
                created_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
            session.add(new_user)
            await session.commit()

    await message.answer(WELCOME_TEXT, reply_markup=main_menu)
