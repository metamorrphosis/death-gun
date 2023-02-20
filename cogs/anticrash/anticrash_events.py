import discord
from discord.ext import commands
from datetime import datetime, timedelta


class AnticrashEventsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id != 837941760193724426:
            return
        
        if member.bot:
            if not(member.public_flags.verified_bot):
                logs = await member.guild.audit_logs(limit = 1, action = discord.AuditLogAction.bot_add).flatten()
                member_add = logs[0].user

                try:
                    await member_add.ban(reason = 'Добавление не верефицированого бота')
                    await member.ban(reason = 'Не верифицированый бот')
                except Exception as e:
                    print(e)
                
                channel = member.guild.get_channel(1053963528735838220)
                await channel.send(f'**Попытка краша**\nТолько что {member_add.mention} (`{member_add}` | `{member_add.id}`) пытался добавить бота {member.mention} (`{member}` | `{member.id}`) на сервер. Оба участника были забанены (наверное)')


def setup(bot):
    bot.add_cog(AnticrashEventsCog(bot))
