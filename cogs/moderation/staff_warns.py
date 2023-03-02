import os
from typing import Union

import discord
import asyncstdlib
from discord.ext import commands, pages

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
    async def staff_warn_command(self, ctx, member: Union[discord.Member, str] = None, *, reason = None):
        usage_field = discord.EmbedField(
            name = 'Использование команды',
            value = f'`{_prefix}выговор <ник, упоминание или ID участника> [причина (не обязательно)]`',
        )

        roles_object = staff_roles_util.Roles(ctx.guild)
        staff_roles = roles_object.get_all_staff_roles()[4:]
    

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
        
        if ctx.author.top_role.position <= member.top_role.position:
            return await ctx.error_reply(description = 'Нельзя выдать выговор участнику, у которого позиция высшей роли такая же, либо выше чем у вас')
                        
        if reason is None:
            reason = 'Причина отсутствует'
        
        warns = await self.db.get_warns(member = member)

        if len(warns) == 10:
            return await ctx.error_reply(
                description = 'Нельзя выдать более 10 выговоров одному участнику'
            )
        
        _id = await self.db.insert_warn(
            author = ctx.author,
            member = member,
            reason = reason
        )

        await ctx.success_reply(
            description = f'Участник {member.mention} (`{member}`) получил выговор номер **{_id}**'
        )
    
    @commands.command(aliases = ['свыговор', 'снятьвыговор'])
    @commands.guild_only()
    async def remove_staff_warn_command(self, ctx, _id = None):
        usage_field = discord.EmbedField(
            name = 'Использование команды',
            value = f'`{_prefix}свыговор <номер выговора>`',
        )

        roles_object = staff_roles_util.Roles(ctx.guild)
        staff_roles = roles_object.get_all_staff_roles()[4:]
    

        check_roles = roles_object.roles_check(
            member = ctx.author,
            roles_list = staff_roles
        )

        roles_mention = ', '.join(role.mention for role in staff_roles)

        if len(check_roles) == 0:
            return await ctx.error_reply(description = f'Эта команда доступна только для следующих ролей:\n {roles_mention}')
        
        if _id is None:
            return await ctx.error_reply(description = 'Вы не указали номер выговора', fields = [usage_field])

        if not _id.isdigit():
            return await ctx.error_reply(description = 'Номер выговора должен быть положительным числом', fields = [usage_field])
        
        _id = int(_id)

        if await self.db.warns.find_one({"_id": _id}) is None:
            return await ctx.error_reply(description = 'Выговор с таким номером не найден', fields = [usage_field])
        
        member_id = await self.db.remove_warn(
            _id = _id
        )

        member = ctx.guild.get_member(member_id)

        if member is None:
            member = f'<@{member_id}> (`{member_id}`)'
        else:
            member = f'<@{member_id}> (`{member}`)'
        
        await ctx.success_reply(
            description = f'Выговор с номером **{_id}** снят. Он принадлежал участнику {member}'
        )
    
    @commands.command(aliases = ['свыговоры'])
    @commands.guild_only()
    async def all_staff_warns_command(self, ctx):
        roles_object = staff_roles_util.Roles(ctx.guild)
        staff_roles = roles_object.get_all_staff_roles()
    

        check_roles = roles_object.roles_check(
            member = ctx.author,
            roles_list = staff_roles
        )

        roles_mention = ', '.join(role.mention for role in staff_roles)

        if len(check_roles) == 0:
            return await ctx.error_reply(description = f'Эта команда доступна только для следующих ролей:\n {roles_mention}')
        
        warns = self.db.warns

        _pages = []
        _fields = []

        for index, i in asyncstdlib.enumerate(warns, start = 1):
            if index % 10 == 0:
                _embed = discord.Embed(
                    title = 'Все выговоры',
                    color = 0xffdbb8,
                    timestamp = datetime.now(),
                    fields = _fields
                )
                _embed.set_footer(text = ctx.author, icon_url = ctx.author.display_avatar.url)

                _pages.append(_embed)
                _field.clear()
            
            warn_author_id = i["author"]
            warn_author = ctx.guild.get_member(warn_author_id)

            if warn_author is None:
                warn_author = f'<@{warn_author_id}> (`{warn_author_id}`)'
            else:
                warn_author = f'<@{warn_author_id}> (`{warn_author}`)'
            
            warn_member_id = i["member"]
            warn_member = ctx.guild.get_member(warn_member_id)

            if warn_member is None:
                warn_member = f'<@{warn_member_id}> (`{warn_member_id}`)'
            else:
                warn_member = f'<@{warn_member_id}> (`{warn_member}`)'
            
            _fields.append(
                discord.EmbedField(
                    name = f'Выговор **{i["_id"]}** ― <t:{i["time"]}:F>',
                    value = f'**Автор:** {warn_author}\n' \
                            f'**Кому:** {warn_member}\n' \
                            f'**Причина:** {i["reason"]}'
                )
            )
        
        page_buttons = [
            pages.PaginatorButton("prev", emoji = discord.PartialEmoji.from_str('<:left:1080904814461993000>'), style = discord.ButtonStyle.green),
            pages.PaginatorButton("page_indicator", style = discord.ButtonStyle.gray, disabled = True),
            pages.PaginatorButton("next", emoji = discord.PartialEmoji.from_str('<:right:1080904828923936890>'), style = discord.ButtonStyle.green)
        ]

        paginator = pages.Paginator(
            pages = _pages,
            use_default_buttons = False,
            custom_buttons = page_buttons,
            loop_pages = True,
        )

        await paginator.send(ctx)


    
def setup(bot):
    bot.add_cog(StaffWarnsCog(bot))