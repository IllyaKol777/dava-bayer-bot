from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🛍 Магазин"), KeyboardButton(text="🚚 Доставка і Оплата")],
        [KeyboardButton(text="📞 Контакти")],
        #[KeyboardButton(text="📰 Акції і новини"), KeyboardButton(text="📣 Поділитися магазином")]
        [KeyboardButton(text="📣 Поділитися магазином")]
    ],
    resize_keyboard=True
)

shop_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🛒 Кошик")],
        [KeyboardButton(text="👖 Штани"), KeyboardButton(text="👕 Худі"), KeyboardButton(text="🩳 Шорти")],
        [KeyboardButton(text="👟 Взуття"), KeyboardButton(text="🧢 Аксесуари")],
        [KeyboardButton(text="🎩 Шапки"), KeyboardButton(text="🧤 Рукавиці"), KeyboardButton(text="👚 Футболки")],
        [KeyboardButton(text="🧥 Куртки / Жилетки")],
        [KeyboardButton(text="🔙 Назад")]
    ],
    resize_keyboard=True
)
