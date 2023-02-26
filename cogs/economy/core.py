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
        
        roles_object = staff_roles_util.Roles(ctx.guild)
        staff_roles = roles_object.get_all_staff_roles()[7:]
        
        check_roles = roles_object.roles_check(
            member = ctx.author,
            roles_list = staff_roles
        )

        roles_mention = ', '.join(role.mention for role in staff_roles)

        if len(check_roles) == 0:
            return await ctx.error_reply(f'Эта команда доступна только для следующих ролей:\n {roles_mention}')
        
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
    
    @commands.command(aliases = ['remove-money', 'rm', 'забрать-деньги', 'забратьденьги', 'ремувмоней', 'монейремув'])
    @commands.guild_only()
    async def removemoney(self, ctx, member: Union[discord.Member, str] = None, value = None):
        usage_field = discord.EmbedField(
            name = 'Использование команды',
            value = f'`{_prefix}remove-money <ник, упоминание или ID участника> <количество>`',
        )
        
        roles_object = staff_roles_util.Roles(ctx.guild)
        staff_roles = roles_object.get_all_staff_roles()[7:]
        
        check_roles = roles_object.roles_check(
            member = ctx.author,
            roles_list = staff_roles
        )

        roles_mention = ', '.join(role.mention for role in staff_roles)

        if len(check_roles) == 0:
            return await ctx.error_reply(description = f'Эта команда доступна только для следующих ролей:\n {roles_mention}')

        if member is None:
            return await ctx.error_reply(description = 'Вы не указали участника, у которого необходимо забрать валюту', fields = [usage_field])
        
        if not(isinstance(member, discord.Member)):
            return await ctx.error_reply(description = 'Участник не найден')

        if value is None:
            return await ctx.error_reply(description = 'Вы не указали количество валюты', fields = [usage_field])

        if not(value.isdigit()):
            return await ctx.error_reply(description = 'Вы указали не правильное количество валюты. Оно должно быть положительным', fields = [usage_field])
        
        value = int(value)

        if value >= 100_000_000_000_000_000:
            return await ctx.error_reply(description = f'Число не может быть больше 100,000,000,000,000,000 {_currency}')

        await self.db.remove_money(
            member = member,
            value = value
        )

        await ctx.success_reply(
            description = f'Забрал {value:,} {_currency} у {member.mention} (`{member}`)'
        )
        
        
    
    @commands.command(aliases = ['reset-money', 'rsm', 'сброс-денег', 'сбросденьги', 'ресетмоней', 'ресет-моней'])
    @commands.guild_only()
    async def resetmoney(self, ctx, member: Union[discord.Member, str] = None):
        usage_field = discord.EmbedField(
            name = 'Использование команды',
            value = f'`{_prefix}reset-money <ник, упоминание или ID участника>`',
        )
        
        roles_object = staff_roles_util.Roles(ctx.guild)
        staff_roles = roles_object.get_all_staff_roles()[7:]
        
        check_roles = roles_object.roles_check(
            member = ctx.author,
            roles_list = staff_roles
        )

        roles_mention = ', '.join(role.mention for role in staff_roles)

        if len(check_roles) == 0:
            return await ctx.error_reply(description = f'Эта команда доступна только для следующих ролей:\n {roles_mention}')
        
        if member is None:
            return await ctx.error(description = 'Вы не указали участника, которому необходимо сбросить валюту', fields = [usage_field])
        
        if not(isinstance(member, discord.Member)):
            return await ctx.error(description = 'Участник не найден')

        value_before = await self.db.reset_money(
            member = member
        )

        await ctx.success(
            description = f'Баланс участника {member.mention} (`{member}`) обнулен. До обнуления у него было {value_before:,} {_currency}'
        )


def setup(bot):
    bot.add_cog(EconomyCog(bot))