import discord
from discord.ext import commands

class FunCommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commadns.guild_only()
    @commands.has_guild_permissions( administrator = True )
    async def say(self, ctx, *, args):
        await ctx.message.delete()
        await ctx.send(args)


def load(bot):
    bot.add_Cog(FunCommandsCog(bot))