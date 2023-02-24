import io

import discord
import psutil
from discord.ext import commands, tasks
from PIL import Image, ImageFont, ImageDraw

class TechnoCommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @tasks.loop(seconds = 100)
    async def banner_update(self):
        guild = self.bot.get_guild(921653080607559681)
        image = Image.open('resources/banner.png')
        
        image_draw = ImageDraw.Draw(image)
        
        _font = ImageFont.truetype('resources/BacknotesRegular.otf', size = 200)
        voice_font = ImageFont.truetype('resources/BacknotesRegular.otf', size = 220)
        
        temp = Image.new('RGBA', (500, 200), (0,0,0,0))
        dr = ImageDraw.Draw(temp)
        dr.text((0, 0), str(len(guild.members)), font = _font)

        temp = temp.rotate(-8, expand = 1)

        image.paste(temp, (460, 695), temp)
        
        voice_members = sum([len(voice.members) for voice in guild.voice_channels])
        temp_voice = Image.new('RGBA', (500, 200), (0,0,0,0))
        dr = ImageDraw.Draw(temp_voice)
        dr.text((0, 0), str(voice_members), font = voice_font)

        temp_voice = temp_voice.rotate(10, expand = 1)

        image.paste(temp_voice, (1490, 675), temp_voice)
        
        saved_image = io.BytesIO()
        image.save(saved_image, format = 'PNG')
        saved_image = saved_image.getvalue()
        
        await guild.edit(banner = saved_image)
        
    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions( administrator = True )
    async def say(self, ctx, *, args):
        await ctx.message.delete()
        await ctx.send(args)
    
    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions( administrator = True )
    async def emojis(self, ctx):
        if ctx.guild.id != 1075448549187256380: return
        await ctx.message.delete()
        await ctx.channel.purge(limit = 200)
        for i in ctx.guild.emojis:
            await ctx.send(str(i))
            await ctx.send(f'\{i}')
     
    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions( administrator = True )
    async def get_json_embed(self, ctx, message_id: int):
        message = await ctx.channel.fetch_message(message_id)
        print()
        print([embed.to_dict() for embed in message.embeds])
    
    @commands.command(aliases = ['ботстатистика', 'ботс', 'ботстат'])
    @commands.guild_only()
    async def stats_bot(self, ctx): 
        async with ctx.channel.typing(): 
            CPU = psutil.cpu_percent(interval = 2) 
            _fields = [
                discord.EmbedField(name = 'CPU', value = f'{CPU} %'),
                discord.EmbedField(name = 'Пинг', value = f'{int(self.bot.latency * 1000)} мс'),
                discord.EmbedField(name = 'Бот был запущен', value = f'<t:{self.bot.uptime}:F>')
            ]
            await ctx.neutral_reply(fields = _fields)
    
    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions( administrator = True )
    async def banner(self, ctx):
        image = Image.open('resources/banner.png')
        
        image_draw = ImageDraw.Draw(image)
        
        _font = ImageFont.truetype('resources/BacknotesRegular.otf', size = 200)
        voice_font = ImageFont.truetype('resources/BacknotesRegular.otf', size = 320)
        
        image_draw.text((470, 720), str(len(ctx.guild.members)), font = _font)
        
        voice_members = sum([len(voice.members) for voice in ctx.guild.voice_channels])
        image_draw.text((1490, 660), str(voice_members), font = voice_font)
        
        image.save('resources/temp_banner.png', format='PNG')
        
        await ctx.reply(file = discord.File(fp = 'resources/temp_banner.png'))
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.banner_update.start()

def setup(bot):
    bot.add_cog(TechnoCommandsCog(bot))
