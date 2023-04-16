import asyncio

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


    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if after.guild.id != 921653080607559681:
            return
        
        if before.roles == after.roles: return
        
        before_adm_roles = 0
        after_adm_roles = 0
        
        for i in before.roles:
            if i.permissions.administrator == True:
                before_adm_roles += 1
        for i in after.roles:
            if i.permissions.administrator == True:
                after_adm_roles += 1
        
        if after_adm_roles > before_adm_roles:
            await asyncio.sleep(2)
            logs = await after.guild.audit_logs(limit = 1, action = discord.AuditLogAction.member_role_update).flatten()
            logs = logs[0]
            user = logs.user
            
            if user.id not in [659728796437708800, 971749397262127144, 1076195979751067771, 983675453988544532, 1075867179137900584, 310848622642069504]:
                try:
                    await user.ban(reason = 'Неразрешенная выдача прав администратора')
                except:
                    pass
                try:
                    await after.ban(reason = 'Неразрешенная выдача прав администратора')
                except:
                    pass
                channel = after.guild.get_channel(1053963528735838220)
                await channel.send(f'**Попытка краша**\nТолько что {logs.user.mention} (`{logs.user}`) пытался выдать права администратора {after.mention} (`{after}`). Оба участника были забанены')
    
    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        if after.guild.id != 921653080607559681:
            return
            
        perms_before = before.permissions
        perms_after = after.permissions
        
        perms_difference = [x[0] for x in after.permissions if x not in before.permissions and x[1]]
        print(perms_difference)
        print(type(perms_difference[0]))
        print(perms_before)
        print(type(perms_before))
        if not perms_difference:
            return
       
        perms_danger = ['administrator',
                                      'ban_members',
                                      'kick_members',
                                      'manage_channels,
                                      'manage_emojis',
                                      'manage_emojis_and_stickers',
                                      'manage_events',
                                      'manage_guild',
                                      'manage_messages',
                                      'manage_nicknames',
                                      'manage_permissions',
                                      'manage_roles',
                                      'manage_threads',
                                      'manage_webhooks',
                                      'mention_everyone',
                                      'moderate_members']
        
        print(perms_danger)
        for i in perms_danger:
            if i in perms_difference:
                logs = await after.guild.audit_logs(limit = 1, action = discord.AuditLogAction.role_update).flatten()
                logs = logs[0]
                user = logs.user
                
                try:
                    await user.ban(reason = 'Неразрешенная выдача прав')
                except:
                    pass
                
               
                await after.edit(permissions = perms_before)
                      
                channel = after.guild.get_channel(1053963528735838220)
                await channel.send(f'**Попытка краша**\nТолько что {logs.user.mention} (`{logs.user}`) пытался выдать краш права на роль `{after.name}`')

def setup(bot):
    bot.add_cog(AnticrashEventsCog(bot))
