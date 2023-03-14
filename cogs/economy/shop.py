import os
import aiohttp
from datetime import datetime

import discord
from discord.ext import commands

from utils import economy_db
from utils.unb_api import update_money
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
                description = description,
                fields = fields
            )
            start_embed.set_image(url = 'https://media.discordapp.net/attachments/1053963528735838220/1076218146505101492/1676660790819.png')

            return start_embed

        _embeds = [
            get_embed(
                title = 'Магазин донатной валюты DeathGun',
                fields = [
                    discord.EmbedField(
                        name = '<:gicon2:1075458949089853610> Спонсорские роли',
                        value = f'> <:godicon:1079082853834436608>・<@&1054133641220980838> — 399{_currency} / месяц\n' \
                                f'> <:absolute:1075469414008356934>・<@&1054133671839420526> — 299{_currency} / месяц\n' \
                                f'> <:blessed:1075469590794092544>・<@&1054134326394110053> — 219{_currency} / месяц\n' \
                                f'> <:faboulous:1075469381129228368>・<@&1054134307280662558> — 169{_currency} / месяц\n' \
                                f'> <:prime:1075469094683422750>・<@&1054134320962474054> — 89{_currency} / месяц'
                    )
                ]
            ),

            get_embed(
                title = '<:gicon2:1075458949089853610> Другое',
                description = f'> <:tochkaicon:1075037704556904529><@&1074035806429249606> — 99{_currency} / навсегда\n' \
                              f'> <:tochkaicon:1075037704556904529><@&1074035980174106706> — 249{_currency} / навсегда\n' \
                              f'> <:tochkaicon:1075037704556904529><@&1074035881297596417> — 149{_currency} / навсегда\n' \
                              f'> <:tochkaicon:1075037704556904529><@&1053765580701831168> — 349{_currency} / до снятия'
            ),

            get_embed(
                title = '<:gicon2:1075458949089853610> Казино',
                description = f'> <:tochkaicon:1075037704556904529>500<:dgsakura:1074019983010582550>  —  1{_currency}'
            )
        ]

        await ctx.reply(embeds = _embeds, view = ShopSelectMenuView())
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


class ShopSelectMenuView(discord.ui.View):
    def __init__(self):
        super().__init__(
            timeout = 90
        )
    
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        
        await self.message.edit(view = self)

    @discord.ui.select(
        placeholder = 'Выберите товар...',
        min_values = 1,
        max_values = 1,
        custom_id = 'shop_select_menu',
        options = [
            discord.SelectOption(
                value = 'casino',
                label = 'Казино',
                description = 'Монеты в боте UnbelievaBoat',
                emoji = discord.PartialEmoji.from_str('<:tochkaicon:1075458720659689533>')            
            ),
        ]
    )
    async def select_callback(self, select, interaction):
        if select.values[0] == 'casino':
            await interaction.response.send_modal(CasinoModal())


class CasinoModal(discord.ui.Modal):
    def __init__(self) -> None:
        self.db = economy_db.EconomyDB()
        super().__init__(
            discord.ui.InputText(
                label = 'Количество донаткоинов на обмен',
                placeholder = 'Пример: 50',
                min_length = 1,
                max_length = 25,
                style = discord.InputTextStyle.short,
                required = True,
            ),
            title = 'Казино'
        )

    async def callback(self, interaction):
        member_bal = await self.db.get_money(member = interaction.user)
        member_bal = member_bal["bal"]

        _value = self.children[0].value

        if not _value.isdigit():
            return await interaction.response.send_message(f'Вы указали не положительное число.\n'
                                                            'Пожалуйста попробуйте ещё раз указав число',
                                                            ephemeral = True)
        
        _value = int(_value)

        if _value == 0:
            return await interaction.response.send_message(f'Число должно быть больше 0',
                                                            ephemeral = True)
        
        if member_bal < _value:
            await interaction.response.send_message(f'У вас нету столько донаткоинов\n' \
                                                    f'Ваш текущий баланс: **{member_bal}{_currency}**\n' \
                                                    f'Вы попытались обменять: **{_value}{_currency}**\n' \
                                                    f'Пожалуйста, введите суму меньше', 
                                                    ephemeral = True)
        
        await self.db.remove_money(member = interaction.user, value = _value)
        await update_money(
            member = interaction.user,
            amount = _value,
            reason = 'Обмен донаткоинов'
        )
        
        await interaction.response.send_message('Обмен произошел успешно', ephemeral = True)


def setup(bot):
    bot.add_cog(ShopCog(bot))