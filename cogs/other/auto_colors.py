import discord
from discord.ext import commands

from utils.other import auto_role


class AutoColorsView(discord.ui.View):
    def __init__(self):
        super().__init__(
            timeout = None,
        )


class AutoColorsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions( administrator = True )
    async def colors(self, ctx):
        await ctx.message.delete()
        _embed = discord.Embed().from_dict({'image': {'url': 'https://cdn.discordapp.com/attachments/1053963528735838220/1075127926053404682/colors.png', 'proxy_url': 'https://media.discordapp.net/attachments/1053963528735838220/1075127926053404682/colors.png', 'width': 2000, 'height': 500}, 'fields': [], 'color': 15645576, 'type': 'rich'})

        _view = AutoColorsView()
        emojis = ['❤️', '🧡', '💛', '💚', '💙', '💜', '💗', '🤍', '🖤']
        role_ids = [1074053302788038788,
                   1074053304457363566,
                   1074053299747164432,
                   1074053305711464558,
                   1074053528961691750,
                   1074053306986541156,
                   1074053535001497650,
                   1074053526612881508,
                   1074053260622704652
        ]
        for _emoji, role_id in zip(emojis, role_ids):
            print(_emoji)
            _button = discord.ui.Button(
                custom_id = str(role_id),
                style = discord.ButtonStyle.gray,
                emoji = _emoji
            )
            _button.callback = auto_role
        await ctx.send(embed = _embed)
    
    
    @commands.Cog.listener()
    async def on_ready(self):
        pass

def setup(bot):
    bot.add_cog(AutoColorsCog(bot))