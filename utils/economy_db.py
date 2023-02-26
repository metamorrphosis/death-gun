import os

import asyncio
from datetime import datetime, timedelta
from dotenv import load_dotenv

import discord
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()


class EconomyDB:
    def __init__(self):
        self.cluster = AsyncIOMotorClient(os.getenv("MONGODB_LINK"))
        self.balances = self.cluster["economy"]["balances"]
    
    async def insert_member(self, *, member: discord.Member) -> bool:
        if await self.balances.find_one({"_id": member.id}) is None:
            new_member = {}
            new_member["_id"] = member.id
            new_member["bal"] = 0
            await self.balances.insert_one(new_member)
            return True
        else:
            return False
    
    async def add_money(self, *, member: discord.Member, value: int) -> bool:
        await self.insert_member(member = member)
        await self.balances.update_one(
            {"_id": member.id},
            {"$inc": {"bal": value}}
        )
        return True
    
    async def remove_money(self, *, member: discord.Member, value: int) -> bool:
        await self.insert_member(member = member)
        await self.balances.update_one(
            {"_id": member.id},
            {"$dec": {"bal": value}}
        )
        return True
    
    async def reset_money(self, *, member: discord.Member) -> int:
        await self.insert_member(member = member)
        
        bal_before = await self.balances.find_one({"_id": member.id})
        
        await self.balances.update_one(
            {"_id": member.id},
            {"$set": {"bal": 0}}
        )
        
        return bal_before["bal"]
    
    async def get_money(self, *, member: discord.Member):
        await self.insert_member(member = member)
        return await self.balances.find_one({"_id": member.id})