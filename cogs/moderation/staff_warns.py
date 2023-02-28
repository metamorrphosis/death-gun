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
                descripiton = 'У данного участника отсутствуют выговоры'
            )
        


def setup(bot):
    bot.add_cog()