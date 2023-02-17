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
            color = 0x1f86ff,
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
       print(f'{self.user} | {self.user.id} - запущен' \
               f'Пинг: {int(self.latency * 100)} мс' \
               f'Кол-во выгруженных файлов: {len(self.bot.extensions)}, когов: {len(self.bot.cogs)}' \
               '————————————————————')
       
       await self.bot.change_presence(activity=discord.Game(name=f'{os.getenv("BOT_PREFIX")}help'), status = discord.Status.dnd)
   
   def load_extensions(self):
       for filename in os.listdir('./cogs'):
           if filename.endswith('.py'):
               self.load_extension(f'cogs.{filename[:-3]}')
               print(f'"{filename[:-3]}" загружен')

main_bot = MainBot()
main_bot.remove_command('help')


async def clear(self, amout=1000):
    await self.channel.purge(limit=amout)

async def info(self,member:discord.Member):
        emb = discord.Embed(title='Информация о пользователе', color=) #Выстави color
        await self.channel.purge(limit=0)
        emb.add_field(name="Присоеденился к Death Gun", value=member.joined_at, inline=False)
        emb.add_field(name="Никнейм:", value=member.display_name, inline=False)
        emb.add_field(name= "Id:", value=member.id, inline=False)
        emb.add_field(name= "Дата регистрации в Discord", value=member.created_at.strftime("%a,%#d %B %Y, %I:%M %p UTC"), inline=False)
        emb.set_thumbnail(url=member.avatar_url)
        emb.set_author(name=self.message.author, icon_url=self.message.author.avatar_url)
        await self.reply(embed = embed)

async def help( self ):
        emb = discord.Embed( title = '✅ Информация о командах сервера', color=344462)
        emb.add_field( name = '{}clear'.format(os.getenv()'BOT_PREFIX')), value = 'Очистка чата одной командой', inline = False)
        emb.add_field( name = '{}kick'.format(os.getenv('BOT_PREFIX')), value = 'Кикнуть участника сервера', inline = False)
        emb.add_field( name = '{}mute'.format(os.getenv('BOT_PREFIX')), value = 'Выдать мут участнику сервера', inline = False)
        emb.add_field( name = '{}unmute'.format(os.getenv('BOT_PREFIX')), value = 'Размутить пользователя', inline = False)
        emb.add_field( name = '{}ban'.format(os.getenv('BOT_PREFIX')), value = 'Выдать блокировку')
        emb.add_field( name = '{}jail'.format(os.getenv('BOT_PREFIX')), value = 'Посадить пользователя в карцер')
        emb.add_field( name = '{}warn'.format(os.getenv('BOT_PREFIX')), value = 'Выдать warn(доступ только для высшей администрации)', inline = False)
        emb.add_field( name = '{}warns'.format(os.getenv('BOT_PREFIX')), value = 'Посмотреть список warns у staff', inline = False)
        emb.add_field( name = '{}unwarn'.format(os.getenv('BOT_PREFIX')), value = 'Снять warn(доступ только для высшей администрации)', inline = False)
        emb.set_thumbnail(url = self.author.avatar_url)
        emb.add_field( name = '{}info'.format(), value = 'Показать подробную информацию об участнике', inline = False)
        await self.author.send(embed = emb) 
#Добавляем туда все команды которые сделаем/сделали


# main_bot.load_extensions()
main_bot.run(os.getenv('BOT_TOKEN'))
