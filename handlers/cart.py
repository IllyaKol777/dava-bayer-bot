from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy import select, delete
from sqlalchemy.exc import NoResultFound
from database import async_session
from models import Cart, Product
from sqlalchemy.orm import selectinload

router = Router()

@router.callback_query(F.data.startswith("add_to_cart:"))
async def add_to_cart(call: CallbackQuery):
    user_id = call.from_user.id
    product_id = int(call.data.split(":")[1])

    async with async_session() as session:
        result = await session.execute(
            select(Cart).where(Cart.user_id == user_id, Cart.product_id == product_id)
        )
        cart_item = result.scalar_one_or_none()

        if cart_item:
            cart_item.quantity += 1
        else:
            session.add(Cart(user_id=user_id, product_id=product_id, quantity=1))

        await session.commit()

    await call.answer("Товар додано в кошик ✅", show_alert=False)


@router.message(F.text == "🛒 Кошик")
async def show_cart(message: Message):
    user_id = message.from_user.id

    async with async_session() as session:
        result = await session.execute(
            select(Cart)
            .where(Cart.user_id == user_id)
            .options(selectinload(Cart.product))
        )
        cart_items = result.scalars().all()

    if not cart_items:
        await message.answer("Ваша корзина порожня 🛒")
        return

    total = 0
    for item in cart_items:
        subtotal = item.quantity * item.product.price
        total += subtotal

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🗑 Видалити", callback_data=f"remove_from_cart:{item.product_id}")]
        ])

        await message.answer(
            f"<b>{item.product.name}</b>\n💰 Ціна: {item.product.price} грн\n🔢 Кількість: {item.quantity}\n📦 Сума: {subtotal} грн",
            reply_markup=keyboard,
            parse_mode="HTML"
        )

    checkout_btn = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Оформити замовлення", callback_data="order")]
    ])
    await message.answer(f"Загальна сума: <b>{total}</b> грн", parse_mode="HTML", reply_markup=checkout_btn)


@router.callback_query(F.data.startswith("remove_from_cart:"))
async def remove_from_cart(call: CallbackQuery):
    user_id = call.from_user.id
    product_id = int(call.data.split(":")[1])

    async with async_session() as session:
        await session.execute(
            delete(Cart).where(Cart.user_id == user_id, Cart.product_id == product_id)
        )
        await session.commit()

    await call.answer("Товар видалено 🗑")
    await call.message.delete()


