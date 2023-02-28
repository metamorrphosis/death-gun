import os
from typing import Union

import discord
from discord.ext import commands

from utils import staff_warns_db
from utils import staff_roles as staff_roles_util

_prefix = os.getenv('BOT_PREFIX')

class StaffWarnsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = staff_warns_db.StaffWarnsDB()
    
    @commands.command(aliases = ['выговоры'])
    @commands.guild_only()
    async def staff_warns_command(self, ctx, _member: discord.Member = None):
        roles_object = staff_roles_util.Roles(ctx.guild)
        staff_roles = roles_object.get_all_staff_roles()
    

        check_roles = roles_object.roles_check(
            member = ctx.author,
            roles_list = staff_roles
        )

        roles_mention = ', '.join(role.mention for role in staff_roles)

        if len(check_roles) == 0:
            return await ctx.error_reply(description = f'Эта команда доступна только для следующих ролей:\n {roles_mention}')
        
        member = _member or ctx.author

        warns = await self.db.get_warns(member = member)

        if len(warns) == 0:
            return await ctx.neutral_reply(
                title = f'Выговоры {member}',
                description = 'У данного участника отсутствуют выговоры'
            )
        
        _fields = []

        for i in warns:
            warn_author_id = i["author"]
            warn_author = ctx.guild.get_member(warn_author_id)

            if warn_author is None:
                warn_author = f'<@{warn_author_id}> (`{warn_author_id}`)'
            else:
                warn_author = f'<@{warn_author_id}> (`{warn_author}`)'
            
            _fields.append(
                discord.EmbedField(
                    name = f'Выговор **{i["_id"]}** ― <t:{i["time"]}:F>',
                    value = f'**Автор:** {warn_author}\n' \
                            f'**Причина:** {i["reason"]}'
                )
            )
        
        await ctx.neutral_reply(
            title = f'Выговоры {member}',
            fields = _fields
        )
    
    @commands.command(aliases = ['выговор'])
    @commands.guild_only()
    async def staff_warn_command(self, ctx, member: Union[discord.Member, str] = None, reason = None):
        usage_field = discord.EmbedField(
            name = 'Использование команды',
            value = f'`{_prefix}выговор <ник, упоминание или ID участника> [причина (не обязательно)]`',
        )

        roles_object = staff_roles_util.Roles(ctx.guild)
        staff_roles = roles_object.get_all_staff_roles()[5:]
    

        check_roles = roles_object.roles_check(
            member = ctx.author,
            roles_list = staff_roles
        )

        roles_mention = ', '.join(role.mention for role in staff_roles)

        if len(check_roles) == 0:
            return await ctx.error_reply(description = f'Эта команда доступна только для следующих ролей:\n {roles_mention}')
        
        if member is None:
            return await ctx.error_reply(description = 'Вы не указали участника, которому необходимо выдать выговор', fields = [usage_field])

        if not(isinstance(member, discord.Member)):
            return await ctx.error_reply(description = 'Участник не найден', fields = [usage_field])

        if reason is None:
            reason = 'Причина отсутствует'
        
        warns = await self.db.get_warns(member = member)

        if len(warns) == 10:
            return await ctx.error_reply(
                description = 'Нельзя выдать более 10 выговоров одному участнику'
            )
        
        _id = await self.db.insert_warn(
            author = ctx.author
            member = member
            reason = reason
        )

        await ctx.success_reply(
            description = f'Участник {member.mention} (`{member}`) получил выговор номер **{_id}**'
        )

        

        


def setup(bot):
    bot.add_cog(StaffWarnsCog(bot))