import os
import asyncio
from datetime import datetime, timedelta

import discord
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()


class TicketsDB:
    def __init__(self):
        self.cluster = AsyncIOMotorClient(os.getenv('MONGODB_LINK'))
    
    async def insert_ticket(self, *, author, who_claimed = None, open_time):
        
        await self.cluster["tickets"]["tickets_list"].update_one({"_id": 0}, {"$inc": {"nmr": 1}})
        ticket_id = await self.cluster["tickets"]["tickets_list"].find_one({"_id": 0})
        ticket_id = ticket_id["nmr"]
        
        new_ticket = {}
        new_ticket["_id"] = ticket_id
        new_ticket["author"] = int(author.id)
        new_ticket["who_claimed"] = int(who_claimed.id) if who_claimed else 0
        new_ticket["open_time"] = int(open_time)
        await self.cluster["tickets"]["tickets_list"].insert_one(new_ticket)
        
        guild = author.guild
        log_channel = guild.get_channel(1073961351115972608)
        emblog = discord.Embed(
            title = 'Тикет открыт',
            color = 0x00ff00,
            timestamp = datetime.now()
        )
        emblog.add_field(
            name = 'Автор тикета',
            value = f'{author.mention} | `{author}` | `{author.id}`',
            inline = False
        )
        emblog.add_field(
            name = 'Айди тикета',
            value = ticket_id,
            inline = False
        )
        await log_channel.send(embed = emblog)
        return ticket_id
    
    async def delete_ticket(self, *, ticket_channel, closed_by):
        ticket_id = self.get_ticket_id(ticket_channel)
        guild = ticket_channel.guild
        
        ticket_db = await self.cluster["tickets"]["tickets_list"].find_one({"_id": ticket_id})

        author = guild.get_member(ticket_db["author"])

        if author is None:
            author_field = f'<@{ticket_db["author"]}> | `Данный участник покинул сервер` | `{ticket_db["author"]}`'
        else:
            author_field = f'{author.mention} | `{author}` | `{author.id}`'
        

        if ticket_db["who_claimed"] != 0:
            who_claimed = guild.get_member(ticket_db["who_claimed"])
            if who_claimed is None:
                who_claimed_field = f'<@{ticket_db["who_claimed"]}> | `Данный участник покинул сервер` | `{ticket_db["who_claimed"]}`'
            else:
                who_claimed_field = f'{who_claimed.mention} | `{who_claimed}` | `{who_claimed.id}`' 
        else:
            who_claimed_field = 'Никто'

        log_channel = guild.get_channel(1073961351115972608)
        emblog = discord.Embed(
            title = 'Тикет закрыт',
            color = 0xff0000,
            timestamp = datetime.now()
        )
        emblog.add_field(
            name = 'Автор тикета',
            value = author_field,
            inline = False
        )
        emblog.add_field(
            name = 'Кто принял тикет',
            value = who_claimed_field,
            inline = False
        )
        emblog.add_field(
            name = 'Кто закрыл тикет',
            value = f'{closed_by.mention} | `{closed_by}` | `{closed_by.id}`',
            inline = False
        )
        emblog.add_field(
            name = 'Дата открытия тикета',
            value = f'<t:{ticket_db["open_time"]}:f>',
            inline = False
        )
        emblog.add_field(
            name = 'Айди тикета',
            value = ticket_id,
            inline = False
        )
        
        await self.cluster["tickets"]["tickets_list"].delete_one({"_id": ticket_id})
        
        messages = await ticket_channel.history(limit=2000).flatten()
        await ticket_channel.delete(reason = 'Тикет закрыт')
        
        messages = messages[::-1]
        fp = f'tickets-log/ticket-{ticket_id}-log.txt'
        
        with open(fp, 'w+') as f:
            f.write(f'Айди тикета: {ticket_id}\nАвтор тикета: {ticket_db["author"]}\nДата открытия тикета: {datetime.fromtimestamp(ticket_db["open_time"]) + timedelta(hours = 3)} МСК\n\n\n——————— Тикет открыт ———————\n\n')
            
            for message in messages:
                if message.content:
                    dt = message.created_at + timedelta(hours = 3)
                    dt = dt.strftime('%d.%m %H:%M:%S МСК')
                    f.write(f'[{message.author} | {message.author.id} — {dt}]\n{message.content}\n\n')
            f.write('——————— Тикет закрыт ———————')
        
        await log_channel.send(embed = emblog, file = discord.File(fp = fp, filename = f'ticket-{ticket_id}-log.txt'))
    
    def get_ticket_id(self, ticket_channel):
        return int(''.join(x for x in ticket_channel.name if x.isdigit()))
    
    async def new_claimed_member(self, member):
        if await self.cluster["tickets"]["claimed_count"].find_one({"_id": member.id}) is None:
            new_member = {}
            new_member["_id"] = member.id
            new_member["all_claimed"] = 0
            await self.cluster["tickets"]["claimed_count"].insert_one(new_member)
            return True
        else:
            return False
    
    async def get_claimed_data(self, member):
        await self.new_claimed_member(member)
        return await self.cluster["tickets"]["claimed_count"].find_one({"id": member.id})
            
    async def claim_ticket(self, *, ticket_channel, who_claimed):
        await self.new_claimed_member(who_claimed)
        await self.cluster["tickets"]["claimed_count"].update_one({"_id": who_claimed.id}, {"$inc": {"all_claimed": 1}})
        
        ticket_id = self.get_ticket_id(ticket_channel)
        
        await self.cluster["tickets"]["tickets_list"].update_one({"_id": ticket_id}, {"$set": {"who_claimed": who_claimed.id}})
        
        guild = ticket_channel.guild
        log_channel = guild.get_channel(1073961351115972608)
        emblog = discord.Embed(
            title = 'Тикет принят',
            color = 0xffee00,
            timestamp = datetime.now()
        )
        emblog.add_field(
            name = 'Кто принял тикет',
            value = f'{who_claimed.mention} | `{who_claimed}` | `{who_claimed.id}`',
            inline = False
        )
        emblog.add_field(
            name = 'Айди тикета',
            value = ticket_id,
            inline = False
        )
        await log_channel.send(embed = emblog)
        return True
