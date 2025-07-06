from aiogram import Router, F
from aiogram.types import Message
from utils.texts import DELIVERY_TEXT, PAYMENT_TEXT, CONTACT_TEXT, NEWS_TEXT, SHARE_TEXT
from keyboards.reply import main_menu
from aiogram.types import InputMediaPhoto
from aiogram.types import FSInputFile


router = Router()

@router.message(F.text == "🚚 Доставка і Оплата")
async def delivery_info(message: Message):
    await message.answer(DELIVERY_TEXT)
    await message.answer(PAYMENT_TEXT)

@router.message(F.text == "📞 Контакти")
async def contact_info(message: Message):
    await message.answer_photo(
        photo=FSInputFile("images/logo.png"),
        caption=CONTACT_TEXT
    )

@router.message(F.text == "📰 Акції і новини")
async def news(message: Message):
    await message.answer(NEWS_TEXT)

@router.message(F.text == "📣 Поділитися магазином")
async def share_bot(message: Message):
    await message.answer(SHARE_TEXT)
