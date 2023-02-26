import os
from typing import Union

import discord
from discord.ext import commands

from utils import economy_db

_prefix = os.getenv('BOT_PREFIX')
_currency = os.getenv('CURRENCY')


class EconomyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = economy_db.EconomyDB()

    @commands.command(aliases = ['money', 'bal', 'бал', 'баланс'])
    @commands.guild_only()
    async def balance(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        
        member_bal = await self.db.get_money(member = member)
        
        await ctx.neutral_reply(
            title = f'Баланс {member}',
            fields = [
                discord.EmbedField(
                    name = 'Валюта', 
                    value = f'{_currency}{member_bal["bal"]:,}'
                )
            ]
        )
    
    @commands.command(aliases = ['add-money', 'am', 'выдать-деньги', 'выдатьденьги', 'аддмоней', 'монейадд'])
    @commands.guild_only()
    async def addmoney(self, ctx, member: Union[discord.Member, str] = None, value = None):
        usage_field = discord.EmbedField(
            name = 'Использование команды',
            value = f'`{_prefix}add-money <ник, упоминание или ID участника> <количество>`',
        )

        if member is None:
            return await ctx.error_reply(description = 'Вы не указали участника, которому необходимо выдать валюту', fields = [usage_field])
        
        if not(isinstance(member, discord.Member)):
            return await ctx.error_reply(description = 'Участник не найден')

        if value is None:
            return await ctx.error_reply(description = 'Вы не указали количество валюты', fields = [usage_field])

        if not(value.isdigit()):
            return await ctx.error_reply(description = 'Вы указали не правильное количество валюты. Оно должно быть положительным', fields = [usage_field])
        
        value = int(value)

        if value >= 100_000_000_000_000_000:
            return await ctx.error_reply(description = f'Число не может быть больше 100,000,000,000,000,000 {_currency}')

        await self.db.add_money(
            member = member,
            value = value
        )

        await ctx.success_reply(
            description = f'Выдал {value:,} {_currency} {member.mention} (`{member}`)'
        )
    
    '''
    @commands.command(aliases = ['reset-money', 'rm', 'сброс-денег', 'сбросденьги', 'ресетмоней', 'ресет-моней'])
    @commands.guild_only()
    @commands.has_guild_permissions( administrator = True )
    async def resetmoney(self, ctx, member: Union[discord.Member, str] = None):
        usage_field = discord.EmbedField(
            name = 'Использование команды',
            value = f'`{prf}reset-money <ник, упоминание или ID участника>`',
        )
        examples_field = discord.EmbedField(
            name = 'Примеры использования команды',
            value = f'`{prf}reset-money @Петя228` — сбросит все деньги пети228\
            \n\n`{prf}add-money 1007615585506566205` — сбросит все деньги участнику с данным ID'
        )

        if member is None:
            return await ctx.error(description = 'Вы не указали участника, которому необходимо сбросить валюту в первом аргументе', fields = [usage_field, examples_field])
        
        if not(isinstance(member, discord.Member)):
            return await ctx.error(description = 'Участник не найден')

        value_before = await self.db.reset_money(
            member = member
        )

        await ctx.success(
            description = f'Баланс участника {member.mention} (`{member}`) обнулен. До обнуления у него всего было {nc(str(value_before))}<:vajno_2:1018512718585679882>'
        )
    '''

    
    
def setup(bot):
    bot.add_cog(EconomyCog(bot))