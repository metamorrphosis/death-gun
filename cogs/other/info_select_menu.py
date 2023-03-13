import discord 
from discord.ext import commands

info_picture = {'image': {'url': 'https://cdn.discordapp.com/attachments/1053963528735838220/1075113889127211119/-2.png', 'proxy_url': 'https://media.discordapp.net/attachments/1053963528735838220/1075113889127211119/-2.png', 'width': 2000, 'height': 500}, 'fields': [], 'color': 15645576, 'type': 'rich'}
info_text = {'image': {'url': 'https://cdn.discordapp.com/attachments/1053963528735838220/1076218146505101492/1676660790819.png', 'proxy_url': 'https://media.discordapp.net/attachments/1053963528735838220/1076218146505101492/1676660790819.png', 'width': 756, 'height': 3}, 'fields': [], 'color': 15645576, 'type': 'rich', 'description': '**<:tochkaicon:1075458720659689533> Медиа** - информация о социальных сетях ДезГана\n**<:tochkaicon:1075458720659689533> Роли** - информация об основных ролях сервера\n**<:tochkaicon:1075458720659689533> Развлечения** - информация о развлечениях сервера и как ими пользоваться', 'title': 'Выбери нужный тебе раздел'}

entertainment_picture = {'image': {'url': 'https://cdn.discordapp.com/attachments/1053963528735838220/1075121660098773094/fun.png', 'proxy_url': 'https://media.discordapp.net/attachments/1053963528735838220/1075121660098773094/fun.png', 'width': 2000, 'height': 500}, 'fields': [], 'color': 15645576, 'type': 'rich'}
entertainment_text = {'image': {'url': 'https://cdn.discordapp.com/attachments/1053963528735838220/1076218146505101492/1676660790819.png', 'proxy_url': 'https://media.discordapp.net/attachments/1053963528735838220/1076218146505101492/1676660790819.png', 'width': 756, 'height': 3}, 'fields': [], 'color': 15645576, 'type': 'rich', 'description': '> <:playingcards:1076710725466193981> Блэкджек:\n> \n> <:tochkaicon:1075458720659689533>Чтобы выиграть, необходимо собрать блэкджек либо набрать больше очков, чем у дилера. Но ты проиграешь, > если наберёшь больше 21 очка.\n> \n> <:tochkaicon:1075458720659689533>.bj [ставка]  - начать игру;\n> <:tochkaicon:1075458720659689533>Hit  - взять ещё одну карту;\n> <:tochkaicon:1075458720659689533>Stand  - закончить игру;\n> <:tochkaicon:1075458720659689533>Double Down  - удвоить ставку, взять одну карту, затем закончить игру.\n> \n> <:minusicon_2:1075458893674721310> Мультипликатор выплат -  [х 2] \n> \n> \n> <:rhombus:1076712028674199632> Рулетка:\n> .roulette [ставка] <место на столе>  - начать игру.\n> \n> <:minusicon_2:1075458893674721310> Мультипликаторы выплат:\n> <:tochkaicon:1075458720659689533>[х 36]  Случайное число (от 0 до 36)\n> <:tochkaicon:1075458720659689533>[х 3]  Дюжины (1-12, 13-24, 25-36)\n> <:tochkaicon:1075458720659689533>[х 3]  Столбцы (1st, 2nd, 3rd)\n> <:tochkaicon:1075458720659689533>[x 2]  Половины (1-18, 19-36)\n> <:tochkaicon:1075458720659689533> х 2]  Чётное / нечётное число (even, odd)\n> <:tochkaicon:1075458720659689533>[х 2]  Цвета (red, black)'}

roles_embeds = [{'image': {'url': 'https://media.discordapp.net/attachments/1053963528735838220/1076556870308864090/roles2.png?width=1440&height=360', 'proxy_url': 'https://media.discordapp.net/attachments/1053963528735838220/1076556870308864090/roles2.png', 'width': 1440, 'height': 360}, 'fields': [], 'color': 15645576, 'type': 'rich'}, {'image': {'url': 'https://cdn.discordapp.com/attachments/1053963528735838220/1076218146505101492/1676660790819.png', 'proxy_url': 'https://media.discordapp.net/attachments/1053963528735838220/1076218146505101492/1676660790819.png', 'width': 756, 'height': 3}, 'fields': [], 'color': 15645576, 'type': 'rich', 'title': '<:tochkaicon:1075037704556904529> **Роли сервера**'}, {'image': {'url': 'https://cdn.discordapp.com/attachments/1053963528735838220/1076218146505101492/1676660790819.png', 'proxy_url': 'https://media.discordapp.net/attachments/1053963528735838220/1076218146505101492/1676660790819.png', 'width': 756, 'height': 3}, 'fields': [], 'color': 15645576, 'type': 'rich', 'description': '> <:tech:1084471574524071966>・<@&957249264751378492> - Люди отвечающие за все на сервере, по всем вопросам к ним.\n> <:cur:1084471636490723378>・<@&1019585554016391199> - Люди отвечающие за стафф сервера, все вопросы по поводу стаффа/жб на стафф, можно подать в тикете, позвав куратора.\n> <:mod:1084471614541938738>・<@&1053692457625333830> - Модераторы сервера, помогают младшему по роли персоналу\n> <:control:1084471271573704784>・<@&1053766515700273172> - Люди прошедшие испытательный срок, следят за чатом.\n> <:sup:1084471223204970569>・<@&1053765580701831168> - Люди, находящиеся на испытательном сроке.', 'title': '<:gicon2:1075458949089853610> Роли персонала'}, {'image': {'url': 'https://cdn.discordapp.com/attachments/1053963528735838220/1076218146505101492/1676660790819.png', 'proxy_url': 'https://media.discordapp.net/attachments/1053963528735838220/1076218146505101492/1676660790819.png', 'width': 756, 'height': 3}, 'fields': [], 'color': 15645576, 'type': 'rich', 'description': '> <:godicon:1079082853834436608>・<@&1054133641220980838> - Самая премиальная покупная роль - подробности в <#1073948924261453914>\n> <:absolute:1075469414008356934>・<@&1054133671839420526> - Покупная роль - подробности в <#1073948924261453914>\n> <:blessed:1075469590794092544>・<@&1054134326394110053> - Покупная роль - подробности в <#1073948924261453914>\n> <:faboulous:1075469381129228368>・<@&1054134307280662558> - Покупная роль - подробности в <#1073948924261453914>\n> <:prime:1075469094683422750>・<@&1054134320962474054> - Покупная роль - подробности в <#1073948924261453914>', 'title': '<:gicon2:1075458949089853610> Спонсорские роли'}, {'image': {'url': 'https://cdn.discordapp.com/attachments/1053963528735838220/1076218146505101492/1676660790819.png', 'proxy_url': 'https://media.discordapp.net/attachments/1053963528735838220/1076218146505101492/1676660790819.png', 'width': 756, 'height': 3}, 'fields': [], 'color': 15645576, 'type': 'rich', 'description': '> <:godchat:1079705741293797426>・<@&1054031984642498581> - за 70 уровень \n> <:selestial:1079705700051189760>・<@&1054031979676434443> - за 60 уровень \n> <:galaxy:1079705677146099732>・<@&1054031708292390983> - за 50 уровень  \n> <:supreme:1079705655176331315>・<@&1054031261452218460> - за 40 уровень \n> <:wardenvoice:1079705624771833887>・<@&1054027513472483379> - за 30 уровень \n> <:conversable:1079705592433754202>・<@&1054026990287597599> - за 25 уровень \n> <:amiable:1079705566605221918>・<@&1054026382453264405> - за 20 уровень \n> <:jovial:1079705537568055316>・<@&1054026168296296458> - за 15 уровень \n> <:sociable:1079705515698946109>・<@&1054025902285140028> - за 10 уровень \n> <:communicative:1079705483595763755>・<@&1054025732227072000> - за 5 уровень', 'title': '<:gicon2:1075458949089853610> Роли за опыт'}, {'image': {'url': 'https://cdn.discordapp.com/attachments/1053963528735838220/1076218146505101492/1676660790819.png', 'proxy_url': 'https://media.discordapp.net/attachments/1053963528735838220/1076218146505101492/1676660790819.png', 'width': 756, 'height': 3}, 'fields': [], 'color': 15645576, 'type': 'rich', 'description': '> <:you:1084471237394305064>・<@&1054134700874150008> - Роль за 5000 подписчиков на площадке YouTube.\n> <:ttw:1084471258458107994>・<@&1054134710122577922> - Роль за 1500 фолловеров на площадке Twich\n> <:tt:1084471209313447997>・<@&1054134714539184219> - Роль за 20.000 подписчиков на площадке TikTok', 'title': '<:gicon2:1075458949089853610> Интегрированные роли'}, {'image': {'url': 'https://cdn.discordapp.com/attachments/1053963528735838220/1076218146505101492/1676660790819.png', 'proxy_url': 'https://media.discordapp.net/attachments/1053963528735838220/1076218146505101492/1676660790819.png', 'width': 756, 'height': 3}, 'fields': [], 'color': 15645576, 'type': 'rich', 'description': '> <:tochkaicon:1075037704556904529><@&922493718987145277> - Роль за буст сервера.\n> <:tochkaicon:1075037704556904529><@&1054134705433358397> - Роль для девушек сервера.', 'title': '<:gicon2:1075458949089853610> Особые роли.'}, {'image': {'url': 'https://cdn.discordapp.com/attachments/1053963528735838220/1076218146505101492/1676660790819.png', 'proxy_url': 'https://media.discordapp.net/attachments/1053963528735838220/1076218146505101492/1676660790819.png', 'width': 756, 'height': 3}, 'fields': [], 'color': 15645576, 'type': 'rich', 'description': '> <:tochkaicon:1075037704556904529><@&1073959312717774918> - Роль закрывает доступ к серверу, из-за нарушения правил.', 'title': '<:gicon2:1075458949089853610> Роли наказаний.'}, {'footer': {'text': 'Для получения интегрированных и ролей для девушек -  обращаться в тикет', 'icon_url': 'https://cdn.discordapp.com/attachments/1075455614249086997/1075462392194007070/heart.png', 'proxy_icon_url': 'https://media.discordapp.net/attachments/1075455614249086997/1075462392194007070/heart.png'}, 'image': {'url': 'https://cdn.discordapp.com/attachments/1053963528735838220/1076218146505101492/1676660790819.png', 'proxy_url': 'https://media.discordapp.net/attachments/1053963528735838220/1076218146505101492/1676660790819.png', 'width': 756, 'height': 3}, 'fields': [], 'color': 15645576, 'type': 'rich', 'description': '> <:tochkaicon:1075037704556904529><@&1073939106935099472> - Роль для объединения всех участников.', 'title': '<:gicon2:1075458949089853610> Общая роль.'}]

media_picture = {'image': {'url': 'https://cdn.discordapp.com/attachments/1053963528735838220/1075122743466528809/asdx.png', 'proxy_url': 'https://media.discordapp.net/attachments/1053963528735838220/1075122743466528809/asdx.png', 'width': 2000, 'height': 500}, 'fields': [], 'color': 15645576, 'type': 'rich'}

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
            ),
            discord.SelectOption(
                value = 'media',
                label = 'Медиа',
                description = 'Информация об социальных сетях ДезГана',
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
        elif select.values[0] == 'roles':
            await interaction.response.send_message(embeds = [discord.Embed().from_dict(_dict) for _dict in roles_embeds], ephemeral = True)
        elif select.values[0] == 'media':
            _embeds = [
                discord.Embed().from_dict(media_picture),
            ]
            
            buttons = [
                discord.ui.Button(
                    url = 'https://t.me/DeathGunOfficial',
                    label = 'Telegram',
                    style = discord.ButtonStyle.blurple
                ),
                discord.ui.Button(
                    url = 'https://www.youtube.com/channel/UChTzPTg6ipxybx3ToTUw4HA',
                    label = 'YouTube',
                    style = discord.ButtonStyle.red
                ),
                discord.ui.Button(
                    url = 'https://www.tiktok.com/@nahmnenick',
                    label = 'TikTok',
                    style = discord.ButtonStyle.gray
                )
            ]
            _view = discord.ui.View()
            
            for i in buttons:
                _view.add_item(i)
            
            await interaction.response.send_message(embeds = _embeds, view = _view, ephemeral = True)


def setup(bot):
    bot.add_cog(InfoSelectMenuCog(bot))
