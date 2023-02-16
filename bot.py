import os
import json
from datetime import datetime

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

class ExpandedContext(commands.Context):  
    async def error_reply(self, *, title = '❌ Ошибка', description = None, fields = None):
        embed = discord.Embed(
            title = title,
            color = 0xf03a3a,
            timestamp = datetime.now(),
            description = description,
            fields = fields
        )
        embed.set_footer(text = self.author, icon_url = self.author.display_avatar.url)
        await self.reply(embed = embed)

    async def success_reply(self, *, title = 'Успешно', description = None, fields = None):
        embed = discord.Embed(
            title = title,
            color = 0x9cde6e,
            timestamp = datetime.now(),
            description = description,
            fields = fields
        )
        embed.set_footer(text = self.author, icon_url = self.author.display_avatar.url)
        await self.reply(embed = embed)

    async def neutral_reply(self, *, title = None, description = None, fields = None):
        embed = discord.Embed(
            title = title,
            color = 0xbffed9,
            timestamp = datetime.now(),
            description = description,
            fields = fields
        )
        embed.set_footer(text = self.author, icon_url = self.author.display_avatar.url)
        await self.reply(embed = embed)


class MainBot(commands.Bot):
    async def get_context(self, message: discord.Message, *, cls = ExpandedContext):
        return await super().get_context(message, cls = cls)
   
   async def on_ready(self):
       print(f'{self.user} | {self.user.id} - запущен' \
               f'Пинг: {int(self.latency * 100)} мс' \
               f'Кол-во выгруженных файлов: {len(self.bot.extensions)}, когов: {len(self.bot.cogs)}' \
               '————————————————————')
       
       await self.bot.change_presence(activity=discord.Game(name=f'{os.getenv("BOT_PREFIX")}help'), status = discord.Status.dnd)
   
   def load_extensions(self):
       for filename in os.listdir('./cogs'):
           if filename.endswith('.py'):
               main_bot.load_extension(f'cogs.{filename[:-3]}')
               print(f'"{filename[:-3]}" загружен')

bot_intents = discord.Intents.all()

main_bot = MainBot(
    intents = bot_intents, 
    command_prefix = commands.when_mentioned_or(os.getenv('BOT_PREFIX'))
)
main_bot.remove_command('help')


# load_extensions()
main_bot.run(os.getenv('BOT_TOKEN'))
