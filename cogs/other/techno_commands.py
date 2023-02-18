import discord
from discord.ext import commands

class TechnoCommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions( administrator = True )
    async def say(self, ctx, *, args):
        await ctx.message.delete()
        await ctx.send(args)
    
    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions( administrator = True )
    async def emojis(self, ctx):
        if ctx.guild.id != 1075448549187256380: return
        await ctx.message.delete()
        for i in ctx.guild.emojis:
            await ctx.send(str(i))
            await ctx.send(f'\{i}')


def setup(bot):
    bot.add_cog(TechnoCommandsCog(bot))
