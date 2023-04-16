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
        
        perms_difference = [x for x in after.permissions if x not in before.permissions]
        print(perms_difference)
        print(type(perms_difference[0]))
        print(perms_before)
        print(type(perms_before))
        if not perms_difference:
            return
       
        perms_danger = [discord.Permissions().administrator,
                                      discord.Permissions().ban_members,
                                      discord.Permissions().kick_members,
                                      discord.Permissions().manage_channels,
                                      discord.Permissions().manage_emojis,
                                      discord.Permissions().manage_emojis_and_stickers,
                                      discord.Permissions().manage_events,
                                      discord.Permissions().manage_guild,
                                      discord.Permissions().manage_messages,
                                      discord.Permissions().manage_nicknames,
                                      discord.Permissions().manage_permissions,
                                      discord.Permissions().manage_roles,
                                      discord.Permissions().manage_threads,
                                      discord.Permissions().manage_webhooks,
                                      discord.Permissions().mention_everyone,
                                      discord.Permissions().moderate_members]
        
        if perms_danger in perms_difference:
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
