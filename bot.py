import os
import json
import asyncio
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
            color = 0xffdbb8,
            timestamp = datetime.now(),
            description = description,
            fields = fields
        )
        embed.set_footer(text = self.author, icon_url = self.author.display_avatar.url)
        await self.reply(embed = embed)


class MainBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(
            intents = discord.Intents.all(),
            command_prefix = os.getenv('BOT_PREFIX')
        )
    
    async def get_context(self, message: discord.Message, *, cls = ExpandedContext):
        return await super().get_context(message, cls = cls)
   
    async def on_ready(self):
        print(f'{self.user} | {self.user.id} - запущен\n' \
               f'Пинг: {int(self.latency * 100)} мс\n' \
               f'Кол-во выгруженных файлов: {len(self.extensions)}, когов: {len(self.cogs)}\n' \
               '————————————————————\n')
        
        self.uptime = int(datetime.timestamp(datetime.now()))
        await self.change_presence(activity=discord.Game(name=f'{os.getenv("BOT_PREFIX")}help'), status = discord.Status.dnd)
   
    async def on_message(msg):
        if msg.author.id == 1083785016443666552:
            await msg.delete()
    
    def load_extensions(self):
        for cog_folder_name in os.listdir('./cogs'):
            for cog_file_name in os.listdir(f'./cogs/{cog_folder_name}'):
                if cog_file_name.endswith('.py'):
                    self.load_extension(f'cogs.{cog_folder_name}.{cog_file_name[:-3]}')
                    print(f'"{cog_file_name}" загружен')


main_bot = MainBot()
main_bot.remove_command('help')

main_bot.load_extensions()
main_bot.run(os.getenv('BOT_TOKEN'))
