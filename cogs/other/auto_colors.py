import time

import discord
from discord.ext import commands

from utils.other import auto_role


class AutoColorsView(discord.ui.View):
    def __init__(self):
        super().__init__(
            timeout = None
        )
     
    @discord.ui.button(
        emoji = '❤️', 
        style = discord.ButtonStyle.gray, 
        custom_id = "1074053302788038788",
        row = 0
    )
    async def red(self, button, interaction):
        result = await auto_role(interaction.user, interaction.guild.get_role(int(button.custom_id)))
        await interaction.response.send_message(result, ephemeral = True)
    

    @discord.ui.button(
        emoji = '🧡', 
        style = discord.ButtonStyle.gray, 
        custom_id = "1074053304457363566",
        row = 0
    )
    async def orange(self, button, interaction):
        result = await auto_role(interaction.user, interaction.guild.get_role(int(button.custom_id)))
        await interaction.response.send_message(result, ephemeral = True)
    
    @discord.ui.button(
        emoji = '💛', 
        style = discord.ButtonStyle.gray, 
        custom_id = "1074053299747164432", 
        row = 0
    )
    async def yellow(self, button, interaction):
        result = await auto_role(interaction.user, interaction.guild.get_role(int(button.custom_id)))
        await interaction.response.send_message(result, ephemeral = True)
    
    @discord.ui.button(
        emoji = '💚', 
        style = discord.ButtonStyle.gray, 
        custom_id = "1074053305711464558",
        row = 1
    )
    async def green(self, button, interaction):
        result = await auto_role(interaction.user, interaction.guild.get_role(int(button.custom_id)))
        await interaction.response.send_message(result, ephemeral = True)
    
    @discord.ui.button(
        emoji = '💙', 
        style = discord.ButtonStyle.gray, 
        custom_id = "1074053528961691750",
        row = 1
    )
    async def blue(self, button, interaction):
        result = await auto_role(interaction.user, interaction.guild.get_role(int(button.custom_id)))
        await interaction.response.send_message(result, ephemeral = True)
    
    @discord.ui.button(
        emoji = '💜', 
        style = discord.ButtonStyle.gray, 
        custom_id = "1074053306986541156",
        row = 1
    )
    async def purple(self, button, interaction):
        result = await auto_role(interaction.user, interaction.guild.get_role(int(button.custom_id)))
        await interaction.response.send_message(result, ephemeral = True)
    
    @discord.ui.button(
        emoji = '🖤', 
        style = discord.ButtonStyle.gray, 
        custom_id = "1074053260622704652",
        row = 2
    )
    async def black(self, button, interaction):
        result = await auto_role(interaction.user, interaction.guild.get_role(int(button.custom_id)))
        await interaction.response.send_message(result, ephemeral = True)
    
    @discord.ui.button(
        emoji = '🤍', 
        style = discord.ButtonStyle.gray, 
        custom_id = "1074053526612881508",
        row = 2
    )
    async def white(self, button, interaction):
        result = await auto_role(interaction.user, interaction.guild.get_role(int(button.custom_id)))
        await interaction.response.send_message(result, ephemeral = True)
    
    @discord.ui.button(
        emoji = '💗', 
        style = discord.ButtonStyle.gray, 
        custom_id = "1074053535001497650",
        row = 2
    )
    async def pink(self, button, interaction):
        result = await auto_role(interaction.user, interaction.guild.get_role(int(button.custom_id)))
        await interaction.response.send_message(result, ephemeral = True)


class AutoColorsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions( administrator = True )
    async def colors(self, ctx):
        await ctx.message.delete()
        _embed = discord.Embed().from_dict({'image': {'url': 'https://cdn.discordapp.com/attachments/1053963528735838220/1075127926053404682/colors.png', 'proxy_url': 'https://media.discordapp.net/attachments/1053963528735838220/1075127926053404682/colors.png', 'width': 2000, 'height': 500}, 'fields': [], 'color': 15645576, 'type': 'rich'})

        await ctx.send(embed = _embed, view = AutoColorsView())
    
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(AutoColorsView())

def setup(bot):
    bot.add_cog(AutoColorsCog(bot))