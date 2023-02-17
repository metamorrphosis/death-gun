import discord
from discord.ext import commands

class UserInfoCommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases = ['юзер', 'пользователь'])
    @commadns.guild_only()
    @commands.has_guild_permissions( administrator = True )
    async def user(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        await ctx.neutral_reply(description = f'<t:{member.joined_at.timestamp()}>')


def load(bot):
    bot.add_Cog(UserInfoCommandsCog(bot))