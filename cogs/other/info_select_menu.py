import discord 
from discord.ext import commands

info_picture = {'image': {'url': 'https://cdn.discordapp.com/attachments/1053963528735838220/1075113889127211119/-2.png', 'proxy_url': 'https://media.discordapp.net/attachments/1053963528735838220/1075113889127211119/-2.png', 'width': 2000, 'height': 500}, 'fields': [], 'color': 15645576, 'type': 'rich'}
info_text = {'image': {'url': 'https://cdn.discordapp.com/attachments/1053963528735838220/1076218146505101492/1676660790819.png', 'proxy_url': 'https://media.discordapp.net/attachments/1053963528735838220/1076218146505101492/1676660790819.png', 'width': 756, 'height': 3}, 'fields': [], 'color': 15645576, 'type': 'rich', 'description': '**<:tochkaicon:1075458720659689533> Медиа** - информация о социальных сетях ДезГана\n**<:tochkaicon:1075458720659689533> Роли** - информация об основных ролях сервера\n**<:tochkaicon:1075458720659689533> Развлечения** - информация о развлечениях сервера и как ими пользоваться', 'title': 'Выбери нужный тебе раздел'}

entertainment_picture = {'image': {'url': 'https://cdn.discordapp.com/attachments/1053963528735838220/1075121660098773094/fun.png', 'proxy_url': 'https://media.discordapp.net/attachments/1053963528735838220/1075121660098773094/fun.png', 'width': 2000, 'height': 500}, 'fields': [], 'color': 15645576, 'type': 'rich'}
entertainment_text = {'fields': [], 'color': 15645576, 'type': 'rich', 'description': '> <:playingcards:1076710725466193981> Блэкджек:\n> \n> <:tochkaicon:1075458720659689533>Чтобы выиграть, необходимо собрать блэкджек либо набрать больше очков, чем у дилера. Но ты проиграешь, > если наберёшь больше 21 очка.\n> \n> <:tochkaicon:1075458720659689533>.bj [ставка]  - начать игру;\n> <:tochkaicon:1075458720659689533>Hit  - взять ещё одну карту;\n> <:tochkaicon:1075458720659689533>Stand  - закончить игру;\n> <:tochkaicon:1075458720659689533>Double Down  - удвоить ставку, взять одну карту, затем закончить игру.\n> \n> <:minusicon_2:1075458893674721310> Мультипликатор выплат -  [х 2] \n> \n> \n> <:rhombus:1076712028674199632> Рулетка:\n> .roulette [ставка] <место на столе>  - начать игру.\n> \n> <:minusicon_2:1075458893674721310> Мультипликаторы выплат:\n> <:tochkaicon:1075458720659689533>[х 36]  Случайное число (от 0 до 36)\n> <:tochkaicon:1075458720659689533>[х 3]  Дюжины (1-12, 13-24, 25-36)\n> <:tochkaicon:1075458720659689533>[х 3]  Столбцы (1st, 2nd, 3rd)\n> <:tochkaicon:1075458720659689533>[x 2]  Половины (1-18, 19-36)\n> <:tochkaicon:1075458720659689533> х 2]  Чётное / нечётное число (even, odd)\n> <:tochkaicon:1075458720659689533>[х 2]  Цвета (red, black)'}


class InfoSelectMenuCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions( administrator = True )
    async def info_menu(self, ctx):
        _embeds = [
            discord.Embed().from_dict(info_picture),
            discord.Embed().from_dict(info_text)
        ]
        await ctx.message.delete()
        await ctx.send(embeds = _embeds, view = InfoSelectMenuView())
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(InfoSelectMenuView())


    '''
            discord.SelectOption(
                value = 'media',
                label = 'Медиа',
                description = 'Информация об социальных сетях ДезГана',
                emoji = discord.PartialEmoji.from_str('<:tochkaicon:1075458720659689533>')
            )
            ПОКА ЧТО НЕТУ ХУКА К ЭТОМУ ВАРИАНТУ, ПУСТЬ БУДЕТ В КОМЕНТАРИИ ПОКА ХУК НЕ СДЕЛАЮТ
    '''
class InfoSelectMenuView(discord.ui.View):
    def __init__(self):
        super().__init__(
            timeout = None
        )
    
    @discord.ui.select(
        placeholder = 'Нажми сюда...',
        min_values = 1,
        max_values = 1,
        custom_id = 'info_select_menu',
        options = [
            discord.SelectOption(
                value = 'entertainment',
                label = 'Развлечения',
                description = 'Информация о развлечениях сервера',
                emoji = discord.PartialEmoji.from_str('<:tochkaicon:1075458720659689533>')            
            ),
            discord.SelectOption(
                value = 'roles',
                label = 'Роли',
                description = 'Информация об основных ролях сервера',
                emoji = discord.PartialEmoji.from_str('<:tochkaicon:1075458720659689533>')
            )
        ]
    )
    async def select_callback(self, select, interaction):
        if select.values[0] == 'entertainment':
            _embeds = [
                discord.Embed().from_dict(entertainment_picture),
                discord.Embed().from_dict(entertainment_text)          
            ]
            await interaction.response.send_message(embeds = _embeds, ephemeral = True)


def setup(bot):
    bot.add_cog(InfoSelectMenuCog(bot))
