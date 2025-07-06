from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from keyboards.reply import main_menu
from database import async_session
from models import Cart, Product
from sqlalchemy import select, delete
from datetime import datetime
from sqlalchemy.orm import selectinload

router = Router()

ADMIN_ID = 6314661034  # заміни на свій ID

class OrderState(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()
    waiting_for_address = State()

@router.callback_query(F.data == "order")
async def start_order(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Вкажіть ваше ім'я та прізвище:")
    await state.set_state(OrderState.waiting_for_name)
    await callback.answer()

@router.message(OrderState.waiting_for_name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введіть номер телефону:")
    await state.set_state(OrderState.waiting_for_phone)

@router.message(OrderState.waiting_for_phone)
async def get_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("Введіть адресу доставки та відділення пошти:")
    await state.set_state(OrderState.waiting_for_address)

@router.message(OrderState.waiting_for_address)
async def get_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    data = await state.get_data()

    async with async_session() as session:
        result = await session.execute(
            select(Cart)
            .where(Cart.user_id == message.from_user.id)
            .options(selectinload(Cart.product))
        )
        items = result.scalars().all()

        if not items:
            await message.answer("Ваша корзина порожня ❌")
            await state.clear()
            return

        print(items)
        total = sum(item.quantity * item.product.price for item in items)
        product_list = "\n".join([
            f"• {item.product.name} — {item.product.price} грн × {item.quantity} = {item.quantity * item.product.price} грн"
            for item in items
        ])

        admin_text = (
            f"🛒 НОВЕ ЗАМОВЛЕННЯ:\n\n"
            f"👤 Ім'я: {data['name']}\n📞 Телефон: {data['phone']}\n📍 Адреса: {data['address']}\n\n"
            f"🛍 Товари:\n{product_list}\n\n"
            f"💰 Сума: {total} грн\n"
            f"Telegram: @{message.from_user.username or 'немає'}\n"
            f"ID: {message.from_user.id}"
        )

        await session.execute(delete(Cart).where(Cart.user_id == message.from_user.id))
        await session.commit()

    await message.answer("✅ Дякуємо за замовлення! Ми скоро з вами звʼяжемося.")
    await message.answer("Повертаємо вас у головне меню ⬇️", reply_markup=main_menu)
    await state.clear()

    await message.bot.send_message(chat_id=ADMIN_ID, text=admin_text)
