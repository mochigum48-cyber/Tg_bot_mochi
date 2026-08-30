"""
Reader Odyssey - Professional Premium Bot
Main Entry Point
"""

import logging, asyncio, dns.resolver, os

dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['8.8.8.8', '1.1.1.1']

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from aiogram import Bot, Dispatcher, types
from config import BOT_TOKEN, OWNER_ID
from handlers.user import router as user_router
from handlers.owner import router as owner_router
from handlers.owner_books import router as owner_books_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

dp.include_router(user_router)
dp.include_router(owner_router)
dp.include_router(owner_books_router)

async def set_commands():
    await bot.set_my_commands([BotCommand(command="start", description="စတင်ရန်")])

async def on_startup():
    logger.info("Starting...")
    await set_commands()
    try: await bot.send_message(OWNER_ID, "Bot Started! /panel")
    except: pass
    logger.info("Ready!")

async def handle_health(request):
    return web.Response(text="OK")

async def main():
    # Health check server
    port = int(os.getenv("PORT", 8000))
    app = web.Application()
    app.router.add_get("/", handle_health)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"Health server on port {port}")
    
    # Bot
    dp.startup.register(on_startup)
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
