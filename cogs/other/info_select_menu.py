import json

import discord 
from discord.ext import commands

class InfoSelectMenuCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions( administrator = True )
    async def info_menu(self, ctx):
        with open('resources/embeds/info_main.json') as embed_file:
            embed_json = embed_file.read()
        
        parsed_json = json.loads(embed_json)
        embed = discord.Embed.from_dict(parsed_json)
        await ctx.message.delete()
        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(InfoSelectMenuCog(bot))
