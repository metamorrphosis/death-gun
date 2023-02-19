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
        print(parsed_json)
        print(type(parsed_json))
        embed = discord.Embed().from_dict({'image': {'url': 'https://cdn.discordapp.com/attachments/1053963528735838220/1076218146505101492/1676660790819.png', 'proxy_url': 'https://media.discordapp.net/attachments/1053963528735838220/1076218146505101492/1676660790819.png', 'width': 756, 'height': 3}, 'fields': [], 'color': 15645576, 'type': 'rich', 'description': '**<:tochkaicon:1075458720659689533> Медиа** - информация о социальных сетях ДезГана\n**<:tochkaicon:1075458720659689533> Роли** - информация об основных ролях сервера\n**<:tochkaicon:1075458720659689533> Развлечения** - информация о развлечениях сервера и как ими пользоваться', 'title': 'Выбери нужный тебе раздел'})
        
        await ctx.message.delete()
        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(InfoSelectMenuCog(bot))
