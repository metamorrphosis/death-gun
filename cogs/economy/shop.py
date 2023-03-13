import os
import aiohttp

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

        start_embed = discord.Embed(
            title = title,
            color = 0x9cde6e,
            timestamp = datetime.now(),
            description = description,
            fields = fields
        )
        start_embed.set_footer(text = self.author, icon_url = self.author.display_avatar.url)

        await ctx.reply(
            title = 'Магазин донатной валюты DeathGun'
        )
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