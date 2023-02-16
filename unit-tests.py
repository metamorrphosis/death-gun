import os
import asyncio

from dotenv import load_dotenv

from bot import MainBot

load_dotenv()

main_bot = MainBot()

async def bot_start():
    main_bot.load_extensions()
    main_bot.run(os.getenv('BOT_TOKEN'))
    await main_bot.wait_until_ready()
    main_bot.close()

asyncio.run(bot_start)
