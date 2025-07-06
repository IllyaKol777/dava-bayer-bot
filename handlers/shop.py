from aiogram import Router, F
from aiogram.types import Message
from keyboards.reply import shop_menu
from utils.texts import SHOP_TEXT
from database import async_session
from models import Product
from sqlalchemy import select
from keyboards.inline import product_buttons
from aiogram.types import FSInputFile
import os
import requests
import uuid


router = Router()

@router.message(F.text == "🛍 Магазин")
async def open_shop(message: Message):
    await message.answer(SHOP_TEXT, reply_markup=shop_menu)

@router.message(F.text.in_({"👖 Штани", "👕 Худі", "🩳 Шорти", "👟 Взуття", "🧢 Аксесуари", "🎩 Шапки", "🧤 Рукавиці", "👚 Футболки", "🧥 Куртки / Жилетки"}))
async def show_category(message: Message):
    category = message.text.split(' ', 1)[-1]

    async with async_session() as session:
        result = await session.execute(
            select(Product).where(Product.category == category)
        )
        products = result.scalars().all()

    if not products:
        await message.answer(f"🔍 Наразі немає товарів у категорії <b>{category}</b>.", parse_mode="HTML")
        return

    for product in products:
        url = f"https://dava-bayer.onrender.com{product.photo}"
        
        # Генеруємо унікальну назву
        unique_filename = f"{uuid.uuid4().hex}.jpg"
        caption = f"<b>{product.name}</b>\n{product.description}\n💵 {product.price} грн"

        try:
            # Скачування зображення
            response = requests.get(url)
            if response.status_code != 200:
                await message.answer("Не вдалося завантажити фото 🥲")
                return

            # Збереження у файл
            with open(unique_filename, "wb") as f:
                f.write(response.content)

            # Надсилання в Telegram
            photo = FSInputFile(unique_filename)
            await message.answer_photo(
                photo=photo,
                caption=caption,    
                reply_markup=product_buttons(product.id),
                parse_mode="HTML"
            )

        finally:
            # Видалення файлу
            if os.path.exists(unique_filename):
                os.remove(unique_filename)
