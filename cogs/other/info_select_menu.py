import json

import discord 
from discord.ext import commands

picturue_embed = {'image': {'url': 'https://cdn.discordapp.com/attachments/1053963528735838220/1075113889127211119/-2.png', 'proxy_url': 'https://media.discordapp.net/attachments/1053963528735838220/1075113889127211119/-2.png', 'width': 2000, 'height': 500}, 'fields': [], 'color': 15645576, 'type': 'rich'}
text_embed = {'image': {'url': 'https://cdn.discordapp.com/attachments/1053963528735838220/1076218146505101492/1676660790819.png', 'proxy_url': 'https://media.discordapp.net/attachments/1053963528735838220/1076218146505101492/1676660790819.png', 'width': 756, 'height': 3}, 'fields': [], 'color': 15645576, 'type': 'rich', 'description': '**<:tochkaicon:1075458720659689533> Медиа** - информация о социальных сетях ДезГана\n**<:tochkaicon:1075458720659689533> Роли** - информация об основных ролях сервера\n**<:tochkaicon:1075458720659689533> Развлечения** - информация о развлечениях сервера и как ими пользоваться', 'title': 'Выбери нужный тебе раздел'}
class InfoSelectMenuCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions( administrator = True )
    async def info_menu(self, ctx):
        _embeds = [
            discord.Embed().from_dict(picturue_embed),
            discord.Embed().from_dict(text_embed)
        ]
        await ctx.message.delete()
        await ctx.send(embeds = _embeds)

def setup(bot):
    bot.add_cog(InfoSelectMenuCog(bot))
