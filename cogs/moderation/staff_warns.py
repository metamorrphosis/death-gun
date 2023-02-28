import discord
from discord.ext import commands

from utils import staff_warns_db

class StaffWarnsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = staff_warns_db.StaffWarnsDB()
    
    @commands.command(aliases = ['выговоры'])
    @commands.guild_only()
    async def staff_warns_command(self, ctx, _member: discord.Member = None):
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
    async def staff_warn_command(self, ctx, _member: discord.Member = None, reason = None):

        warns = await self.db.get_warns(member = member)

        if len(warns) == 10:
            return await ctx.error_reply(
                description = 'Нельзя выдать более 10 выговоров одному участнику'
            )
        


def setup(bot):
    bot.add_cog(StaffWarnsCog(bot))