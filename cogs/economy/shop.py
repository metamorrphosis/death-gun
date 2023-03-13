import os
import aiohttp
from datetime import datetime

import discord
from discord.ext import commands

from utils import economy_db
from utils import staff_roles as staff_roles_util

_prefix = os.getenv('BOT_PREFIX')
_currency = os.getenv('CURRENCY')
_unb_api_token = os.getenv('UNB_API_TOKEN')


class ShopCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = economy_db.EconomyDB()
    
    @commands.command(aliases = ['store', 'магазин'])
    @commands.guild_only()
    async def shop(self, ctx):
        await ctx.trigger_typing()

        def get_embed(title = None, description = None, fields = None):
            start_embed = discord.Embed(
                title = title,
                color = 0x9cde6e,
                timestamp = datetime.now(),
                description = description,
                fields = fields
            )
            start_embed.set_footer(text = ctx.author, icon_url = ctx.author.display_avatar.url)
            start_embed.set_image(url = 'https://media.discordapp.net/attachments/1075455614249086997/1075476615758348408/-PhotoRoom.png-PhotoRoom66.png?width=1035&height=60')

            return start_embed

        _embeds = [
            get_embed(
                title = 'Магазин донатной валюты DeathGun'
            )
        ]

        await ctx.reply(embeds = _embeds)
        '''
        TODO:

        ЧЕГО НЕТ В ШОПЕ:
        Личная роль - 99 дон.
        Войс комната - 249 дон.
        В стафф без набора - 349 дон.
        Гильдия - 149 дон.

        ПРИВИЛЕГИИ:
        Prime - 89 дон./мес.
        Fabulous - 169 дон./мес
        Blessed - 219 дон./мес
        Absolute - 299 дон./мес
        God - 399 дон./мес

        КАЗИНО:
        500 лепестков (валюта анбеливы) будет равняться одному донат коину (валюта нашего кастом бота)
        все циферки выше сказал скай
        у анбеливы апи есть, токен в .env уже написан через него обмен валют
        апи анбеливы юзать через aiohttp для асинка
        '''

def setup(bot):
    bot.add_cog(ShopCog(bot))