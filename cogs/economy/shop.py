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

        def get_embed(*, title = None, description = None, fields = None):
            start_embed = discord.Embed(
                title = title,
                color = 0xffca7a,
                timestamp = datetime.now(),
                description = description,
                fields = fields
            )
            start_embed.set_image(url = 'https://media.discordapp.net/attachments/1075455614249086997/1075476615758348408/-PhotoRoom.png-PhotoRoom66.png?width=1035&height=60')

            return start_embed

        _embeds = [
            get_embed(
                title = 'Магазин донатной валюты DeathGun'б
                fields = [
                    discord.EmbedField(
                        title = '<:gicon2:1075458949089853610> Спонсорские роли',
                        description = f'> <:godicon:1079082853834436608>・<@&1054133641220980838> — 399{_currency} / месяц\n> <:absolute:1075469414008356934>・<@&1054133671839420526> — 299{_currency} / месяц\n> <:blessed:1075469590794092544>・<@&1054134326394110053> — 219{_currency} / месяц\n> <:faboulous:1075469381129228368>・<@&1054134307280662558> — 169{_currency} / месяц\n> <:prime:1075469094683422750>・<@&1054134320962474054> — 89{_currency} / месяц'
                    )
                ]
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