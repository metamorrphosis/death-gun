import discord
from discord.commands import option
import config
from utils import tickets_db, my_roles
from datetime import datetime
from discord.ext import commands

class OpenedTicketView(discord.ui.View):
    def __init__(self):
        self.db = tickets_db.TicketsDB()
        super().__init__(timeout = None)
    

    @discord.ui.button(
        emoji = discord.PartialEmoji.from_str('<:asm_stormy_member:1018512431510724658>'), 
        style = discord.ButtonStyle.gray,
        custom_id = "ticket_claim",
        label = 'Принять тикет'
    )
    async def claim_callback(self, button, interaction):
        uroles = my_roles.Roles(interaction.guild)
        staff_roles = uroles.get_all_staff_roles()
        check_roles = uroles.roles_check(
            member = interaction.user,
            roles_list = staff_roles
        )

        roles_mention = ', '.join(role.mention for role in staff_roles)

        if len(check_roles) == 0:
            return await interaction.response.send_message(f'Эта кнопка доступна только для следующих ролей:\n {roles_mention}', ephemeral = True)

        self.children[0].disabled = True
        await interaction.message.edit(view = self)
        await interaction.channel.set_permissions(interaction.user, send_messages=True, read_messages=True)

        ticket_overwrites = {}
        staff_roles = my_roles.Roles(interaction.guild).get_all_staff_roles()[:6]

        await self.db.claim_ticket(
            ticket_channel = interaction.channel,
            who_claimed = interaction.user
        )

        await interaction.response.send_message(f'{interaction.user.mention} (`{interaction.user}`) Будет обслуживать Ваш тикет')

        for i in staff_roles:
            await interaction.channel.set_permissions(i, send_messages = False)
            
    @discord.ui.button(
        emoji = discord.PartialEmoji.from_str('<:asm_stormy_tech:1018512527258304583>'), 
        style = discord.ButtonStyle.gray,
        custom_id = "ticket_close",
        label = 'Закрыть тикет'
    )
    async def close_callback(self, button, interaction):
        uroles = my_roles.Roles(interaction.guild)
        staff_roles = uroles.get_all_staff_roles()
        check_roles = uroles.roles_check(
            member = interaction.user,
            roles_list = staff_roles
        )

        roles_mention = ', '.join(role.mention for role in staff_roles)

        if len(check_roles) == 0:
            return await interaction.response.send_message(f'Эта кнопка доступна только для следующих ролей:\n {roles_mention}', ephemeral = True)

        await self.db.delete_ticket(
            ticket_channel = interaction.channel,
            closed_by = interaction.user
        )    


class StartTicketView(discord.ui.View):
    def __init__(self):
        self.db = tickets_db.TicketsDB()
        self.mention_message = '<@&991219359731163187> <@&989892564691873793> <@&1009021230080348190> <@&989891381575159870>'
        super().__init__(timeout = None)
    
    @discord.ui.button(
        emoji = discord.PartialEmoji.from_str('<:a_to_accept:1020623049231441990>'), 
        style = discord.ButtonStyle.gray,
        custom_id = "open_ticket",
        label = 'Открыть тикет'
    )
    async def callback(self, button, interaction):
        async for i in self.db.cluster.tickets.tickets_list.find():
            if i["_id"] == 0:
                continue
            if i["author"] == interaction.user.id:
                return await interaction.response.send_message('Нельзя открыть более 1 тикета за раз', ephemeral = True)
        
        ticket_category = interaction.guild.get_channel(config.tickets_category)

        ticket_overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True),
        }

        staff_roles = my_roles.Roles(interaction.guild).get_all_staff_roles()[:6]

        if interaction.user.id != 1007615585506566205:
            for i in staff_roles:
                ticket_overwrites[i] = discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True)

        ticket_id = await self.db.insert_ticket(
            author = interaction.user,
            open_time = int(datetime.timestamp(datetime.now()))
        )

        ticket_channel = await ticket_category.create_text_channel(name = f'тикет-{ticket_id}', overwrites = ticket_overwrites)
        
        mention = await ticket_channel.send(self.mention_message)
        embticket = discord.Embed(
            title = f'<:a_notification:1020307597670223922> Открытый тикет',
            description = f'<:e_white_dot:1018821114853601353>Здравствуйте! Вы попали в свой тикет. Модерация поможет вам в кротчайшие сроки. Пока что можете написать цель создания тикета.\n<:c_level_10:1018512555280453712> Примечание:\n<:e_green_dot:1018821297481994280>За попытки обмана администрации выдаётся предупреждение',
            color = 0xbffed9
        )
        embticket.set_image(url = 'https://cdn.discordapp.com/attachments/1017458641537859604/1018492145335816192/SAVE_20220710_205848.jpg')
        await mention.delete() 
        await ticket_channel.send(f'{interaction.user.mention} (`{interaction.user}`)', embed = embticket, view = OpenedTicketView())
        await interaction.response.send_message(f'Тикет успешно создан — {ticket_channel.mention}', ephemeral = True)

        
        



class TicketsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = tickets_db.TicketsDB()

    slash_group = discord.SlashCommandGroup(name = 'ticket', guild_only = True, guild_ids = [837941760193724426])
    
    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions( administrator = True )
    async def ticketstart(self, ctx):
        embticket = discord.Embed(
            title = 'Тикеты',
            description = 'Для открытия тикета используйте кнопку ниже',
            color = 0xbffed9
        )
        embticket.set_image(url = 'https://cdn.discordapp.com/attachments/1017458641537859604/1018492145335816192/SAVE_20220710_205848.jpg')
        await ctx.message.delete()
        await ctx.send(embed = embticket, view = StartTicketView())
    
    @slash_group.command(name = 'close', description = 'Закрывает тикет')
    async def slash_ticket_close(self, ctx):
        uroles = my_roles.Roles(ctx.guild)
        staff_roles = uroles.get_all_staff_roles()
        check_roles = uroles.roles_check(
            member = ctx.author,
            roles_list = staff_roles
        )

        roles_mention = ', '.join(role.mention for role in staff_roles)

        if len(check_roles) == 0:
            return await ctx.send_response(f'Эта команда доступна только для следующих ролей:\n {roles_mention}', ephemeral = True)

        if ctx.channel.category.id != config.tickets_category or ctx.channel.id == config.tickets_channel:
            return await ctx.send_response('Эта команда доступна только в категории тикетов', ephemeral = True)

        await self.db.delete_ticket(
            ticket_channel = ctx.channel,
            closed_by = ctx.author
        )  

        await ctx.send_response('Тикет закрыт')
    
    @slash_group.command(name = 'claim', description = 'Принимает тикет')
    async def slash_ticket_claim(self, ctx):

        uroles = my_roles.Roles(ctx.guild)
        staff_roles = uroles.get_all_staff_roles()
        check_roles = uroles.roles_check(
            member = ctx.author,
            roles_list = staff_roles
        )

        roles_mention = ', '.join(role.mention for role in staff_roles)

        if len(check_roles) == 0:
            return await ctx.send_response(f'Эта команда доступна только для следующих ролей:\n {roles_mention}', ephemeral = True)

        if ctx.channel.category.id != config.tickets_category or ctx.channel.id == config.tickets_channel:
            return await ctx.send_response('Эта команда доступна только в категории тикетов', ephemeral = True)

        ticket_id = self.db.get_ticket_id(ctx.channel)
        db_ticket = await self.db.cluster["tickets"]["tickets_list"].find_one({"_id": ticket_id})

        if db_ticket["who_claimed"] != 0:
            return await ctx.send_response('Данный тикет уже и так принят', ephemeral  = True)

        async for message in ctx.channel.history(limit = 10, oldest_first = True):
            if message.author.id == self.bot.user.id:
                global first_message
                first_message = message
                break
        
        ticket_view = discord.ui.View.from_message(first_message)
        ticket_view.children[0].disabled = True
        await first_message.edit(view = ticket_view)

        await ctx.channel.set_permissions(ctx.author, send_messages=True, read_messages=True)

        await self.db.claim_ticket(
            ticket_channel = ctx.channel,
            who_claimed = ctx.author
        )

        await ctx.send_response(f'{ctx.author.mention} (`{ctx.author}`) Будет обслуживать Ваш тикет')
        
        ticket_overwrites = {}
        staff_roles = my_roles.Roles(ctx.guild).get_all_staff_roles()[:6]

        for i in staff_roles:
            await ctx.channel.set_permissions(i, send_messages = False)
    
    @slash_group.command(name = 'add', description = 'Добавляет пользователя в тикет')
    @option(
        name = 'пользователь',
        description = 'Пользователь, которого необходимо добавить в тикет',
        input_type = discord.Member,
        required = True
        
    )
    async def slash_ticket_add(self, ctx, member: discord.Member):

        uroles = my_roles.Roles(ctx.guild)
        staff_roles = uroles.get_all_staff_roles()
        check_roles = uroles.roles_check(
            member = ctx.author,
            roles_list = staff_roles
        )

        roles_mention = ', '.join(role.mention for role in staff_roles)

        if len(check_roles) == 0:
            return await ctx.send_response(f'Эта команда доступна только для следующих ролей:\n {roles_mention}', ephemeral = True)

        if ctx.channel.category.id != config.tickets_category or ctx.channel.id == config.tickets_channel:
            return await ctx.send_response('Эта команда доступна только в категории тикетов', ephemeral = True)
        
        await ctx.channel.set_permissions(member, read_messages = True, send_messages = True, attach_files = True)
        await ctx.send_response(f'{member.mention} (`{member}`) успешно добавлен в тикет')
    
    @slash_group.command(name = 'remove', description = 'Удаляет пользователя из тикета')
    @option(
        name = 'пользователь',
        description = 'Пользователь, которого необходимо удалить из тикета',
        input_type = discord.Member,
        required = True
        
    )
    async def slash_ticket_remove(self, ctx, member: discord.Member):

        uroles = my_roles.Roles(ctx.guild)
        staff_roles = uroles.get_all_staff_roles()
        check_roles = uroles.roles_check(
            member = ctx.author,
            roles_list = staff_roles
        )

        roles_mention = ', '.join(role.mention for role in staff_roles)

        if len(check_roles) == 0:
            return await ctx.send_response(f'Эта команда доступна только для следующих ролей:\n {roles_mention}', ephemeral = True)

        if ctx.channel.category.id != config.tickets_category or ctx.channel.id == config.tickets_channel:
            return await ctx.send_response('Эта команда доступна только в категории тикетов', ephemeral = True)
        
        await ctx.channel.set_permissions(member, read_messages = False, send_messages = False, attach_files = False)
        await ctx.send_response(f'{member.mention} (`{member}`) успешно удален из тикета')
        

    
    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(StartTicketView(), message_id = 1032738056182181889)
        self.bot.add_view(OpenedTicketView())
    

def setup(bot):
    bot.add_cog(TicketsCog(bot))
