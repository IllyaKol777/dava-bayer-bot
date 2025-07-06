import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from database import init_db
from handlers import start, menu, shop, cart, order

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    await init_db()

    dp.include_routers(
        start.router,
        menu.router,
        shop.router,
        cart.router,
        order.router
    )

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())