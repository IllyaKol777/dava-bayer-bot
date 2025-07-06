from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def product_buttons(product_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛒 Додати в кошик", callback_data=f"add_to_cart:{product_id}")]
    ])
