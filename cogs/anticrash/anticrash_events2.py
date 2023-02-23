from datetime import datetime

import discord
from discord.ext import commands


class AnticrashEventsCog2(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
        self.guild_id = 921653080607559681
        self.white_list = [
            659728796437708800, # qqsky
            971749397262127144, #tamada
            1076195979751067771, # qqsky + dg (owner)
            983675453988544532, # dg
            1075867179137900584 # dg bot (self.bot.user.id)
        ]
        self.admin_channel = 1053963528735838220
    
    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        guild = role.guild
        if guild.id != self.guild_id:
            return
        
        logs = await guild.audit_logs(limit = 1, action = discord.AuditLogAction.role_delete).flatten()
        logs = logs[0]
        user = logs.user

        if user.id in self.white_list:
            return
        
        if not(str(user.id) in self.cd_roles):
            self.cd_roles[str(user.id)] = {}
            self.cd_roles[str(user.id)]["last_update"] = 0
            self.cd_roles[str(user.id)]["count"] = 0
        
        if int(datetime.timestamp(datetime.now())) - self.cd_roles[str(user.id)]["last_update"] > 3600:
            self.cd_roles[str(user.id)]["last_update"] = int(datetime.timestamp(datetime.now()))
            self.cd_roles[str(user.id)]["count"] = 1
        else:
            self.cd_roles[str(user.id)]["count"] += 1
            
            if self.cd_roles[str(user.id)]["count"] == 3:
                
                try:
                    await user.ban(reason = 'Попытка краша путем массового удаления/создания ролей')
                except:
                    pass
                
                channel = guild.get_channel(self.admin_channel)
                await channel.send(f'**Попытка краша**\nТолько что участник {user.mention} (`{user}`) пытался крашнуть сервер путем массового удаления/создания ролей. Участник был забанен')
                
                
                self.cd_roles[str(user.id)]["last_update"] = 0
                self.cd_roles[str(user.id)]["count"] = 0
                
    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        guild = role.guild
        if guild.id != self.guild_id:
            return
        
        logs = await guild.audit_logs(limit = 1, action = discord.AuditLogAction.role_create).flatten()
        logs = logs[0]
        user = logs.user

        if user.id in self.white_list:
            return
        
        if not(str(user.id) in self.cd_roles):
            self.cd_roles[str(user.id)] = {}
            self.cd_roles[str(user.id)]["last_update"] = 0
            self.cd_roles[str(user.id)]["count"] = 0
        
        if int(datetime.timestamp(datetime.now())) - self.cd_roles[str(user.id)]["last_update"] > 3600:
            self.cd_roles[str(user.id)]["last_update"] = int(datetime.timestamp(datetime.now()))
            self.cd_roles[str(user.id)]["count"] = 1
        else:
            self.cd_roles[str(user.id)]["count"] += 1
            
            if self.cd_roles[str(user.id)]["count"] == 3:
                
                try:
                    await user.ban(reason = 'Попытка краша путем массового удаления/создания ролей')
                except:
                    pass
                
                channel = guild.get_channel(self.admin_channel)
                await channel.send(f'**Попытка краша**\nТолько что участник {user.mention} (`{user}`) пытался крашнуть сервер путем массового удаления/создания ролей. Участник был забанен')
                
                
                self.cd_roles[str(user.id)]["last_update"] = 0
                self.cd_roles[str(user.id)]["count"] = 0
    
    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        guild = channel.guild
        if guild.id != self.guild_id:
            return
        
        logs = await guild.audit_logs(limit = 1, action = discord.AuditLogAction.channel_delete).flatten()
        logs = logs[0]
        user = logs.user
        

        if user.id in self.white_list:
            return
        
        if not(str(user.id) in self.cd_channels):
            self.cd_channels[str(user.id)] = {}
            self.cd_channels[str(user.id)]["last_u"] = 0
            self.cd_channels[str(user.id)]["count"] = 0
        
        if int(datetime.timestamp(datetime.now())) - self.cd_channels[str(user.id)]["last_update"] > 7200:
            self.cd_channels[str(user.id)]["last_update"] = int(datetime.timestamp(datetime.now()))
            self.cd_channels[str(user.id)]["count"] = 1
        else:
            self.cd_channels[str(user.id)]["count"] += 1
            
            if self.cd_channels[str(user.id)]["count"] == 2:
                try:
                    await user.ban(reason = 'Попытка краша путем массового удаления/создания каналов')
                except:
                    pass
                channel = guild.get_channel(self.admin_channel)
                await channel.send(f'**Попытка краша**\nТолько что участник {user.mention} (`{user}`) пытался крашнуть сервер путем массового удаления/создания каналов. Участник был забанен')

                self.cd_channels[str(user.id)]["last_update"] = 0
                self.cd_channels[str(user.id)]["count"] = 0
         
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        guild = channel.guild
        if guild.id != self.guild_id:
            return
        
        logs = await guild.audit_logs(limit = 1, action = discord.AuditLogAction.channel_create).flatten()
        logs = logs[0]
        user = logs.user
        

        if user.id in self.white_list:
            return
        
        if not(str(user.id) in self.cd_channels):
            self.cd_channels[str(user.id)] = {}
            self.cd_channels[str(user.id)]["last_u"] = 0
            self.cd_channels[str(user.id)]["count"] = 0
        
        if int(datetime.timestamp(datetime.now())) - self.cd_channels[str(user.id)]["last_update"] > 7200:
            self.cd_channels[str(user.id)]["last_update"] = int(datetime.timestamp(datetime.now()))
            self.cd_channels[str(user.id)]["count"] = 1
        else:
            self.cd_channels[str(user.id)]["count"] += 1
            
            if self.cd_channels[str(user.id)]["count"] == 2:
                try:
                    await user.ban(reason = 'Попытка краша путем массового удаления/создания каналов')
                except:
                    pass
                channel = guild.get_channel(self.admin_channel)
                await channel.send(f'**Попытка краша**\nТолько что участник {user.mention} (`{user}`) пытался крашнуть сервер путем массового удаления/создания каналов. Участник был забанен')

                self.cd_channels[str(user.id)]["last_update"] = 0
                self.cd_channels[str(user.id)]["count"] = 0
                
    @commands.Cog.listener()
    async def on_member_ban(self, guild, member):
        if guild.id != self.guild_id:
            return
        
        logs = await guild.audit_logs(limit = 1, action = discord.AuditLogAction.ban).flatten()
        logs = logs[0]
        user = logs.user
        

        if user.id in self.white_list:
            return
        
        if not(str(user.id) in self.cd_bans):
            self.cd_bans[str(user.id)] = {}
            self.cd_bans[str(user.id)]["last_update"] = 0
            self.cd_bans[str(user.id)]["count"] = 0
        
        if int(datetime.timestamp(datetime.now())) - self.cd_bans[str(user.id)]["last_update"] > 3600:
            self.cd_bans[str(user.id)]["last_update"] = int(datetime.timestamp(datetime.now()))
            self.cd_bans[str(user.id)]["count"] = 1
            
        else:
            self.cd_bans[str(user.id)]["count"] += 1
            if self.cd_bans[str(user.id)]["count"] == 2:
                try:
                    await user.ban(reason = 'Попытка краша путем массового кика/бана участников')
                except:
                    pass
                
                channel = guild.get_channel(996360133288415262)
                await channel.send(f'**Попытка краша**\nТолько что участник {user.mention} (`{user}`) пытался крашнуть сервер путем массового кика/бана участников. Участник был забанен')

                self.cd_bans[str(user.id)]["last_update"] = 0
                self.cd_bans[str(user.id)]["count"] = 0
    
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.cd_roles = {}

        self.cd_channels = {}
        
        self.cd_bans = {}

def setup(bot):
    bot.add_cog(AnticrashEventsCog2(bot))
