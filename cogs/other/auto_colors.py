import time

import discord
from discord.ext import commands

from utils.other import auto_role


class AutoColorsView(discord.ui.View):
    def __init__(self):
        super().__init__(
            timeout = None,
        )

    async def _scheduled_task(self, item: discord.ui.Item, interaction: discord.Interaction):
        try:
            if self.timeout:
                self.__timeout_expiry = time.monotonic() + self.timeout

            allow = await self.interaction_check(interaction)
            if not allow:
                return await self.on_check_failure(interaction)

            await item.callback(interaction, item.custom_id)
        except Exception as e:
            return await self.on_error(e, item, interaction)


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
        iterations, _row = 0, 0
        for _emoji, role_id in zip(emojis, role_ids):
            if iterations % 3 == 0:
                _row += 1

            _button = discord.ui.Button(
                custom_id = str(role_id),
                style = discord.ButtonStyle.gray,
                emoji = _emoji,
                row = _row
            )

            _button.callback = auto_role
            _view.add_item(_button)

            iterations += 1
        
        await ctx.send(embed = _embed, view = _view)
    
    
    @commands.Cog.listener()
    async def on_ready(self):
        pass

def setup(bot):
    bot.add_cog(AutoColorsCog(bot))